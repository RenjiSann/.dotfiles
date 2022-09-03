alias ls='exa'
alias la='exa -a'
alias ll='exa -l --git'
alias lla='exa -la'
alias lh='exa -lh'

alias p3='python3'

#   alias gadd='git add'
#   alias gcm='git commit -m'
#   alias gstt='git status'
#   alias gph='git push'
#   alias gpl='git pull'
alias gpft='git push --follow-tags'

alias matrix='ncmatrix -I wlp1s0 -R red -T yellow'

alias cf='find . -iname "*.[ch]" -or -iname "*.[ch]pp" -or -iname "*.cc" -or -iname "*.hh" -or -iname "*.[ch]xx" | xargs clang-format -i --style=file'

alias gccc='gcc -Wall -Wextra -Werror -pedantic -std=c99'
alias gppp='g++ -Wall -Wextra -Werror -pedantic -std=c++20'

# Rust cargo aliases
alias cgt='cargo test'
alias cgti='cargo test -- --include-ignored'
alias cgb='cargo build'
alias cgc='cargo clean'
