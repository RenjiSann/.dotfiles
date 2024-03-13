extern crate anyhow;
extern crate cstr;
extern crate nix;

use std::{fs::File, io::Write, path::Path, ffi::CStr};

use anyhow::Result;
use cstr::cstr;
use nix::{
    sys::{utsname::uname, ptrace::attach, wait::{waitpid, WaitStatus}},
    unistd::{execvp, fork, ForkResult, Uid, User, Pid},
};

const BIN_FILE: &'static CStr = cstr!("./straceme");

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
            WaitStatus::Exited(pid, exit) => {
                println!("Child process {} exited with exit code {}", pid, exit);
            }
            WaitStatus::Stopped(_, _) => todo!(),
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
