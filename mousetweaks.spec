Name:		mousetweaks
Version:	2.28.2
Release:	1%{?dist}
Summary:	Mouse accessibility support for the GNOME desktop
Group:		User Interface/Desktops
License:	GPLv3 and GFDL
URL:		http://live.gnome.org/Mousetweaks/Home
Source0:	http://download.gnome.org/sources/mousetweaks/2.28/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gettext
BuildRequires:  gnome-doc-utils
BuildRequires:  pkgconfig
BuildRequires:  GConf2-devel
BuildRequires:  gtk2-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXtst-devel
BuildRequires:  libglade2-devel
BuildRequires:  gnome-panel-devel
BuildRequires:  at-spi-devel
BuildRequires:  intltool

Requires(pre):   GConf2
Requires(post):  GConf2
Requires(preun): GConf2

%description
The Mousetweaks package provides mouse accessibility enhancements for
the GNOME desktop, such as performing various clicks without using any
hardware button. The options can be accessed through the Accessibility
tab of the Mouse Preferences of GNOME Control Center or through command-line.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done

%find_lang mousetweaks --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  for f in %{_sysconfdir}/gconf/schemas/mouseweaks.schemas \
	   %{_sysconfdir}/gconf/schemas/pointer-capture-applet.schemas ;
    do
      if [ -f $f ]; then
        gconftool-2 --makefile-uninstall-rule $f >/dev/null
      fi
    done
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/mousetweaks.schemas \
	%{_sysconfdir}/gconf/schemas/pointer-capture-applet.schemas \
	>/dev/null

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/gconf/schemas/mousetweaks.schemas \
	%{_sysconfdir}/gconf/schemas/pointer-capture-applet.schemas \
	>/dev/null
fi

%files -f mousetweaks.lang
%defattr(-,root,root,-)
%doc COPYING COPYING.FDL COPYING.GPL README NEWS
%{_sysconfdir}/gconf/schemas/mousetweaks.schemas
%{_sysconfdir}/gconf/schemas/pointer-capture-applet.schemas
%{_bindir}/dwell-click-applet
%{_bindir}/mousetweaks
%{_bindir}/pointer-capture-applet
%{_libdir}/bonobo/servers/DwellClick_Factory.server
%{_libdir}/bonobo/servers/PointerCapture_Factory.server
%{_datadir}/mousetweaks
%doc %{_mandir}/man1/*

%changelog
* Mon Jan  4 2010 Matthias Clasen <mclasen@redhat.com> 2.28.2-1
- Update to 2.28.2

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-1
- Update to 2.28.1

* Mon Sep 22 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Tue May 26 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Sun Jul 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Use standard icon name

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Thu May 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-3
- Fix a typo

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Make the %%pre script handle missing schema files

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Sat Apr 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Initial packaging
