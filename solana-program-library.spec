%global commit          aaca5353bc7bd273031f5792854902dbe22601e0
%global checkout_date   20220613
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


%prep
%autosetup -p1 -b0 -n %{name}-%{commit}
%autosetup -p1 -b1 -n %{name}-%{commit}

mkdir .cargo
cp %{SOURCE2} .cargo/


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


%changelog
* Mon Jun 13 2022 Ivan Mironov <mironov.ivan@gmail.com> - 0-0.0.20220613gitaaca535
- Initial packaging
