extern crate anyhow;
extern crate cstr;
extern crate nix;

use std::{ffi::CStr, fs::File, io::Write, path::PathBuf};

use anyhow::Result;
use cstr::cstr;
use nix::{
    sys::{
        ptrace::{attach, getregs, setregs, syscall, cont},
        utsname::uname,
        wait::{waitpid, WaitStatus}, signal::Signal,
    },
    unistd::{execvp, fork, getcwd, ForkResult, Pid, Uid, User}, libc::SIGSTOP,
};

const BIN_FILE: &'static CStr = cstr!("./straceme");
const KILL_SYSCALL: u64 = 62;

fn compute_filename() -> Result<String> {
    let uname = uname()?;
    let uid = Uid::current();
    let user = User::from_uid(uid)?.expect("Unable to find user from uid");

    Ok(format!(
        "{}-{}-{}.{}-mysteryfile!!",
        uname.release().to_str().expect("no uname release"),
        uname.nodename().to_str().expect("no uname nodename"),
        uid,
        user.name
    ))
}

fn intercept_child_signals(cpid: Pid) {
    attach(cpid).unwrap();

    let status = waitpid(cpid, None).expect("Waitpid error");
    if let WaitStatus::Stopped(_, Signal::SIGSTOP) = status {
        cont(cpid, None).expect("Continue");
    }

    loop {
        let status = waitpid(cpid, None).expect("Waitpid error");

        match status {
            WaitStatus::Exited(_, exit) => {
                println!(
                    "Child process {} exited with exit code {}",
                    cpid, exit
                );
                break;
            }
            WaitStatus::Stopped(_, signal) => {
                println!("Signal: {:?}", signal);
                // The child process was stopped by tracing
                let mut regs =
                    getregs(cpid).expect("Failed to get child registers");
                if regs.orig_rax == KILL_SYSCALL {
                    println!("Intercepted a kill syscall");
                    // Make the request fail
                    regs.rax = 1;
                    setregs(cpid, regs).expect("Failed to set child registers");
                }

                syscall(cpid, signal).unwrap();
            }
            _ => (),
        }
    }
}

fn main() {
    let filename: String =
        compute_filename().expect("Couldn't create filename");
    let path: PathBuf = getcwd().expect("Failed to get cwd").join(filename);

    // Create the file in sub scope to close the file upon drop.
    {
        let mut file: File = File::options()
            .create(true)
            .write(true)
            .truncate(true)
            .open(path)
            .expect("Failed to create file");

        // Write 493 bytes into the file
        file.write_all(&[b'x'; 493])
            .expect("Couldn't write to file");
    }

    match unsafe { fork().expect("Fork failed") } {
        ForkResult::Parent { child } => intercept_child_signals(child),
        ForkResult::Child => {
            execvp::<&CStr>(BIN_FILE, &[])
                .expect("failed to launch sub-program");
        }
    }
}
