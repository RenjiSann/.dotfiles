extern crate anyhow;
extern crate cstr;
extern crate nix;

use std::{fs::File, io::Write, path::Path, ffi::CStr};

use anyhow::Result;
use cstr::cstr;
use nix::{
    sys::{utsname::uname, ptrace::{attach, getregs, syscall}, wait::{waitpid, WaitStatus}},
    unistd::{execvp, fork, ForkResult, Uid, User, Pid},
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

    loop {
        let status = waitpid(cpid, None).expect("Waitpid error");

        match status {
            WaitStatus::Exited(_, exit) => {
                println!("Child process {} exited with exit code {}", cpid, exit);
            }
            WaitStatus::Stopped(_, signal) => {
                // The child process was stopped by tracing
                let regs = getregs(cpid).expect("Could not get child registers");
                if regs.orig_rax == KILL_SYSCALL {
                    println!("Intercepted a kill syscall");
                }

                syscall(cpid, None).unwrap();
            }
            _ => ()
        }
    }
}

fn main() {
    let filename: String = compute_filename().expect("Couldn't create filename");
    let path: &Path = Path::new(&filename);

    // Create the file in sub scope to close the file upon drop.
    {
        let mut file: File = File::options()
            .create(true)
            .truncate(true)
            .open(path)
            .expect("Could not create file");

        // Write 493 bytes into the file
        file.write_all(&[b'x'; 493])
            .expect("Couldn't write to file");
    }

    match unsafe { fork().expect("Fork failed") } {
        ForkResult::Parent { child } => intercept_child_signals(child),
        ForkResult::Child => {
            execvp::<&CStr>(BIN_FILE, &[]).expect("failed to launch sub-program");
        }
    }
}
