%define         privroot %{?my_privroot}%{?!my_privroot:private}
%define         urlroot %{?my_urlroot}%{?!my_urlroot:mirror.centos.org}
%define         pathroot %{?my_pathroot}%{?!my_pathroot:centos}
%define         MYBUILDIR %{name}-%{version}-%{release}

Name:		%{privroot}-release-scl
Version:	2
Release:	2%{?dist}
Summary:	Private network copy of Software collections from the CentOS SCLo SIG
Url:            http://mirror.centos.org/centos/7/extras/x86_64/Packages/centos-release-scl-%{version}-%{release}.rpm

Group:		System Environment/Base
License:	GPLv2

Source1:        RPM-GPG-KEY-CentOS-SIG-SCLo
Source2:        Private-SCLo-scl.repo
Source3:        GPL


BuildArch:      noarch
BuildRequires:	rpm
Requires:	centos-release

%description
yum Configs and basic docs for Software Collections as delivered via the CentOS SCLo SIG.


%prep
# Nuke stale build-dir
if [[ -d %{MYBUILDIR} ]]
then
   rm -rf %{MYBUILDIR}
fi

# Create new build-dir
install -Ddm 000755 %{MYBUILDIR}
install -Dbm 000644 %{SOURCE2} %{MYBUILDIR}



%build
sed -i '{
         s/__PRIVREPO__/%{privroot}/g
         s/__MIRROR_HOST__/%{urlroot}/g
         s#__PATH_ROOT__#%{pathroot}#g
         /baseurl/s/$/\nskip_if_unavailable=1/
      }' %{MYBUILDIR}/Private-SCLo-scl.repo 


%install
PRIVCAP=$( echo %{privroot} | tr "[:lower:]" "[:upper:]" )
install -Dbm 000644 %{MYBUILDIR}/Private-SCLo-scl.repo %{buildroot}/%{_sysconfdir}/yum.repos.d/${PRIVCAP}-SCLo-scl.repo
install -Dbm 000644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-SCLo
install -Dbm 000644 %{SOURCE3} %{buildroot}/%{_prefix}/share/doc/%{privroot}-release-scl/GPL


%files
%defattr(000644,root,root,000755)
/etc/pki/rpm-gpg/*
/usr/share/doc/%{privroot}-release-scl/*
%doc
%config /etc/yum.repos.d/*



%changelog
