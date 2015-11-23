This page will show you how to build a binary version of QTodoTxt for:
* Mac Os X
* Windows
* Debian

For each environment you have to check before that you can run QTodoTxt from command line with no errors. See [here for more details.](https://github.com/mNantern/QTodoTxt/wiki#quick-run)

# Mac Os X

We will build the package with py2app and [DMG Architect](https://itunes.apple.com/fr/app/dmg-architect-disk-builder/id426104753).

1. From packaging/MacOs run `python setup.py py2app`
2. Open packaging/MacOs/build.dmgpkg with DMG Architect and press the button **Build** and then **Finalize**
3. Binary app is in dist/qtodotxt.app and the package is in your DMG directory (`/Users/matt/Documents/DMG Architect` for me)

# Windows

We will build the package with py2app and [Inno Setup](http://www.jrsoftware.org/isinfo.php).

1. From packaging/Windows run `python.exe setup.py py2exe`
2. Open packaging/Windows/installer.iss with Inno Setup and press the button **Run**
3. The package is in `packaging\Windows\build\installer`

# Debian

And last but never least Linux packaging:

1. Go to packaging/Debian and run as root `python buildDebPackage.py <tag>` . For 1.3.0 you will run `python buildDebPackage.py 1.3.0`.
2. Your package should be in /tmp/. Run the command `lintian <package_path>` to check for errors in packaging.
