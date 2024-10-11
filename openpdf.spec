Name:			openpdf
Version:		1.4.2
Release:		%autorelease
Summary:		The open source successor of iText
License:		LGPL 2.1
URL:			https://github.com/LibrePDF/OpenPDF

Source0:		https://github.com/LibrePDF/OpenPDF/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:		noarch

ExclusiveArch:	%{java_arches} noarch

BuildRequires:	maven-local-openjdk11
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:	mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:	mvn(org.assertj:assertj-core)
BuildRequires:	mvn(org.mockito:mockito-core)
BuildRequires:	mvn(org.hamcrest:hamcrest)
BuildRequires:	mvn(org.bouncycastle:bcprov-jdk18on)
BuildRequires:	mvn(org.bouncycastle:bcpkix-jdk18on)
BuildRequires:	mvn(org.apache.xmlgraphics:fop)
BuildRequires:  mvn(com.ibm.icu:icu4j)
BuildRequires:	mvn(org.jacoco:jacoco-maven-plugin)

%description
OpenPDF is a Java library for creating and editing PDF files with a LGPL and MPL open source license. OpenPDF is the LGPL/MPL open source successor of iText, and is based on some forks of iText 4 svn tag.

%package libs
Summary:		OpenPDF Java library
Requires:		%{name} = %{version}-%{release}

%description libs
OpenPDF is a Java library for creating and editing PDF files with a LGPL and MPL open source license.

%package fonts-extra
Summary:		OpenPDF bundled fonts
Requires:		%{name}-libs = %{version}-%{release}

%description fonts-extra
OpenPDF bundled extra fonts (such as Liberation fonts)

%package javadoc
Summary:		OpenPDF JavaDoc Documentation

%description javadoc
JavaDoc documentation for OpenPDF

%prep
%autosetup -n OpenPDF-%{version}

%mvn_package ":openpdf" %{name}-libs
%mvn_package ":openpdf-fonts-extra" %{name}-fonts-extra
%mvn_package ":openpdf:pom" %{name}

# We're missing these
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-javadoc-plugin

# We do not want these to end up in the requirements
%pom_remove_plugin :maven-clean-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-repository-plugin
%pom_remove_plugin :pitmp-maven-plugin
%pom_remove_plugin :maven-failsafe-plugin

# Disable optional dependency
%pom_remove_dep org.verapdf:validation-model openpdf/pom.xml
rm -f openpdf/src/test/java/com/lowagie/text/validation/PDFValidationTest.java

# Do not build tools and pdf-swing
%pom_disable_module pdf-swing
%pom_disable_module pdf-toolbox

%build
%mvn_build -s -- -Dmaven.compiler.source=9 -Dmaven.compiler.target=9

%install
%mvn_install

%files -f .mfiles-openpdf-parent
%license LICENSE.md
%doc README.md

%files libs -f .mfiles-openpdf-libs
%license openpdf/src/main/resources/META-INF/LGPL-2.1.md

%files fonts-extra -f .mfiles-openpdf-fonts-extra
%license openpdf-fonts-extra/src/main/resources/META-INF/LGPL-2.1.md

%files javadoc -f .mfiles-javadoc

%changelog
%autochangelog
