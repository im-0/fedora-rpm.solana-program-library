%global commit          c38a1b5d6a1a6049b5844aef8e50e889e18918ed
%global checkout_date   20240323
%global short_commit    %(c=%{commit}; echo ${c:0:7})
%global snapshot        .%{checkout_date}git%{short_commit}

Name:       solana-program-library
Version:    0
Release:    0.0%{?snapshot}%{?dist}
Summary:    CLI tools for Solana Program Library

License:    Apache-2.0
URL:        https://github.com/solana-labs/%{name}/
Source0:    https://github.com/solana-labs/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

# $ cargo vendor
# Contains solana-program-library-$COMMIT/vendor/*.
Source1:    %{name}-%{commit}.cargo-vendor.tar.xz
Source2:    config.toml

Patch0: fix-proc-macro-crate.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  openssl-devel

# libudev-devel
BuildRequires:  systemd-devel


%description
CLI tools for Solana Program Library.


%package token
Summary:    CLI tool for Solana Token Program


%description token
CLI tool for Solana Token Program (spl-token).


%package feature-proposal
Summary:    CLI tool for Solana Feature Proposal Program


%description feature-proposal
CLI tool for Solana Feature Proposal Program (spl-feature-proposal).


%package stake-pool
Summary:    CLI tool for Solana Stake Pool Program


%description stake-pool
CLI tool for Solana Stake Pool Program (spl-stake-pool).


%package token-lending
Summary:    CLI tool for Solana Token Lending Program


%description token-lending
CLI tool for Solana Token Lending Program (spl-token-lending).


%package single-pool
Summary:    CLI tool for Solana Single-Validator Stake Pool


%description single-pool
CLI tool for Solana Single-Validator Stake Pool (spl-single-pool).


%package token-upgrade
Summary:    CLI tool for Solana Token Upgrade


%description token-upgrade
CLI tool for Solana Token Upgrade (spl-token-upgrade).


%package transfer-hook
Summary:    CLI tool for Solana Transfer Hook program


%description transfer-hook
CLI tool for Solana Transfer Hook program (spl-transfer-hook).


%prep
%setup -q -D -T -b0 -n %{name}-%{commit}
%setup -q -D -T -b1 -n %{name}-%{commit}

%patch -P 0 -p1

mkdir .cargo
cp %{SOURCE2} .cargo/

# Fix Fedora's shebang mangling errors:
#     *** ERROR: ./usr/src/debug/solana-testnet-1.10.0-1.fc35.x86_64/vendor/ascii/src/ascii_char.rs has shebang which doesn't start with '/' ([cfg_attr(rustfmt, rustfmt_skip)])
find . -type f -name "*.rs" -exec chmod 0644 "{}" ";"


%build
%{__cargo} build %{?_smp_mflags} -Z avoid-dev-deps --frozen --release


%install
mkdir -p %{buildroot}/%{_bindir}

find target/release -mindepth 1 -maxdepth 1 -type d -exec rm -r "{}" \;
rm target/release/*.d
rm target/release/*.rlib

mv target/release/spl-* \
        %{buildroot}/%{_bindir}/


%files token
%{_bindir}/spl-token


%files feature-proposal
%{_bindir}/spl-feature-proposal


%files stake-pool
%{_bindir}/spl-stake-pool


%files token-lending
%{_bindir}/spl-token-lending


%files single-pool
%{_bindir}/spl-single-pool


%files token-upgrade
%{_bindir}/spl-token-upgrade


%files transfer-hook
%{_bindir}/spl-transfer-hook


%changelog
* Sat Mar 23 2024 Ivan Mironov <mironov.ivan@gmail.com> - 0-0.0.20240323gitc38a1b5
- Bump version to current git

* Fri Sep 22 2023 Ivan Mironov <mironov.ivan@gmail.com> - 0-0.0.20230922git88add99
- Bump version to current git

* Mon Jun 13 2022 Ivan Mironov <mironov.ivan@gmail.com> - 0-0.0.20220613gitaaca535
- Initial packaging
