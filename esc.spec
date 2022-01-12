Name:		esc		
Version:	1.1.2
Release:	6
Summary:	esc embeds files into go programs and provides http		
License:	GPL+
URL:		https://github.com/mjibson/esc
Source0:	http://pki.fedoraproject.org/pki/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:	esc
Source2:	esc.desktop
Source3:	esc.png

BuildRequires:  glib2-devel atk-devel pkgconfig nspr-devel nss-devel nss-static
BuildRequires:	pcsc-lite-devel desktop-file-utils dbus-glib-devel glib2-devel gcc-c++
BuildRequires:  opensc gobject-introspection-devel gtk3-devel gjs-devel GConf2-devel
BuildRequires:  chrpath

Requires:	pcsc-lite nss nspr dbus opensc gjs gobject-introspection gtk3 glib2

AutoReqProv: 0

%description
esc embeds files into go programs and provides http.FileSystem interfaces to them.
It adds all named files or files recursively under named directories at the path 
specified. The output file provides an http.FileSystem interface with zero 
dependencies on packages outside the standard library.

%package_help

%prep
%autosetup -n %{name} -p1

%build
./autogen.sh

make

%install
%make_install
install -m 0755 -d %{buildroot}/%{_datadir}/icons/hicolor/48x48/apps
install -m 0755 -d %{buildroot}/%{_datadir}/applications
install -m 0755 -d %{buildroot}/%{_datadir}/pixmaps
install -m 0755 -d %{buildroot}%{_libdir}/%{name}-%{version}

sed -e 's;\$LIBDIR;'%{_libdir}';g'  %{SOURCE1}
install -m 0755 -D %{SOURCE1} %{buildroot}%{_bindir}/%{name}
install -p -D %{buildroot}%{_prefix}/local/bin/* %{buildroot}%{_libdir}/%{name}-%{version}
cp -a %{buildroot}%{_prefix}/local/lib %{buildroot}%{_libdir}/%{name}-%{version}

%delete_la_and_a
rm -rf %{buildroot}/%{_prefix}/local

install -p -m 0755 %{SOURCE3} %{buildroot}/%{_datadir}/icons/hicolor/48x48/apps

pushd %{buildroot}
ln -s %{_datadir}/icons/hicolor/48x48/apps/esc.png usr/share/pixmaps/esc.png
popd

install -m 0755 %{SOURCE2} %{buildroot}/%{_datadir}/applications

chrpath -d %{buildroot}%{_libdir}/%{name}-%{version}/lib/libcoolkeymgr-1.0.so.0.0.0

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "/usr/local/lib" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE

%{_bindir}/%{name}
%{_libdir}/%{name}-%{version}/lib
%{_libdir}/%{name}-%{version}/esc.js
%{_libdir}/%{name}-%{version}/opensc.esc.conf
%{_datadir}/pixmaps/esc.png
%{_datadir}/applications/esc.desktop
%{_datadir}/icons/hicolor/48x48/apps/esc.png
%config(noreplace) /etc/ld.so.conf.d/*

%files help
%defattr(-,root,root)

%changelog
* Wed Jan 12 2022 Ge Wang <wangge20@huawei.com> - 1.1.2-6
- Add chrpath in BuildRequire

* Wed Sep 9 2021 caodongxia <caodongxia@huawei.com> - 1.1.2-5
- Remove rpath

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.1.2-4
- Type: bugfix
- ID: NA
- SUG: NA
- DESC: delete files in help package 

* Thu Nov 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.1.2-3
- Package init
