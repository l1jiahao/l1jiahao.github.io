#!/usr/bin/env bash
# 使用 Homebrew Ruby 3.3，不修改系统 Ruby 或 shell 配置。
set -euo pipefail
cd "$(dirname "$0")/.."
if command -v brew >/dev/null 2>&1; then
  ruby_prefix=$(brew --prefix ruby@3.3 2>/dev/null || true)
  if [[ -x "$ruby_prefix/bin/ruby" ]]; then
    export PATH="$ruby_prefix/bin:$PATH"
  fi
fi
ruby -e 'abort "需要 Ruby >= 3.0；macOS 可运行 brew install ruby@3.3" if RUBY_VERSION.split(".").first.to_i < 3'
# 某些 macOS Command Line Tools 只在 SDK 中提供 C++ 标准库头文件。
if [[ "$(uname -s)" == Darwin ]]; then
  sdk_path=$(xcrun --show-sdk-path)
  if [[ -f "$sdk_path/usr/include/c++/v1/iostream" ]]; then
    export CPLUS_INCLUDE_PATH="$sdk_path/usr/include/c++/v1${CPLUS_INCLUDE_PATH:+:$CPLUS_INCLUDE_PATH}"
  fi
fi
# 安装依赖到忽略目录；锁文件纳入版本控制。
bundle config set --local path vendor/bundle
bundle check >/dev/null 2>&1 || bundle install
if [[ $# -eq 0 ]]; then
  exec bundle exec jekyll serve --host 127.0.0.1
fi
exec bundle exec jekyll "$@"
