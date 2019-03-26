%define         privroot %{?my_privroot}%{?!my_privroot:private}
%define         urlroot %{?my_urlroot}%{?!my_urlroot:mirror.centos.org}
%define         pathroot %{?my_pathroot}%{?!my_pathroot:centos}
%define         MYBUILDIR %{name}-%{version}-%{release}

Name:		%{privroot}-release-storage-common
Version:	2
Release:	2%{?dist}
Summary:	Private network copy of Common release file to establish shared metadata for CentOS Storage SIG
Url:            http://mirror.centos.org/centos/7/extras/x86_64/Packages/centos-release-storage-common-%{version}-%{release}.noarch.rpm


Group:		System Environment/Base
License:	GPLv2

Source1:        RPM-GPG-KEY-CentOS-SIG-Storage
Source2:        Private-Storage-common.repo


BuildArch:      noarch
BuildRequires:	rpm
Requires:	centos-release

Provides:       centos-release-storage-common


%description
Common files needed by other centos-release components in the Storage SIG


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
      }' %{MYBUILDIR}/Private-Storage-common.repo


%install
PRIVCAP=$( echo %{privroot} | tr "[:lower:]" "[:upper:]" )
install -Dbm 000644 %{MYBUILDIR}/Private-Storage-common.repo %{buildroot}/%{_sysconfdir}/yum.repos.d/${PRIVCAP}-SCLo-scl.repo
install -Dbm 000644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-Storage


%files
%defattr(000644,root,root,000755)
/etc/pki/rpm-gpg/*
%doc
%config /etc/yum.repos.d/*



%changelog
