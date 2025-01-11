# Define installer settings
!define APP_NAME "stellabot"
!define APP_VERSION "1.0"
!define APP_PUBLISHER "Your Company"
!define APP_EXE "stellabot.exe"
!define APP_ICON "stellabot.ico"

# Output installer file
OutFile "${APP_NAME} Installer.exe"

# Default installation directory
InstallDir "$PROGRAMFILES\${APP_NAME}"

# Set installer icon
Icon "${APP_ICON}"
UninstallIcon "${APP_ICON}"

# Request administrator privileges
RequestExecutionLevel admin

# Pages to show in the installer
Page directory
Page instfiles

# Uninstaller settings
UninstallText "This will uninstall ${APP_NAME}."

# Installer sections
Section "Install"
    # Create installation directory
    SetOutPath "$INSTDIR"

    # Copy application files
    File "${APP_EXE}"
    File "${APP_ICON}"

    # Create desktop shortcut
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_ICON}"

    # Create start menu shortcut
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_ICON}"

    # Write uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

# Uninstaller section
Section "Uninstall"
    # Delete installed files
    Delete "$INSTDIR\${APP_EXE}"
    Delete "$INSTDIR\${APP_ICON}"
    Delete "$INSTDIR\uninstall.exe"

    # Delete shortcuts
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"

    # Remove installation directory
    RMDir "$INSTDIR"
SectionEnd
