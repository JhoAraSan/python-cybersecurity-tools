
# Guía parcial: Conexión a Exchange (PowerShell) y verificación/instalación de Active Directory

:leftwards_arrow_with_hook: [python-cybersecurity-tools](../README.md)


> **Estado:** borrador parcial (MD). Incluye pasos para: comprobar módulo de Exchange, actualizarlo, conectarse; y traer/instalar el módulo de Active Directory (o alternativas si no está disponible).

---

## 1. Prerrequisitos generales

- **PowerShell 5.1** (Windows) o **PowerShell 7.x**.
- Permisos adecuados para conectarte a **Exchange Online** y consultar **Active Directory**.
- Conectividad de red hacia Microsoft 365 (Exchange) y/o el **Controlador de Dominio**.
- Política de ejecución permitiendo módulos: 

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 2. Exchange Online — módulo `ExchangeOnlineManagement`

### 2.1 Verificar si está instalado
```powershell
# Ver módulos instalados vía PowerShellGet
Get-InstalledModule ExchangeOnlineManagement

# Ver módulos disponibles en el sistema
Get-Module -ListAvailable ExchangeOnlineManagement | Select-Object Name, Version, ModuleBase
```

### 2.2 Instalar (si no está) o actualizar a la última versión
```powershell
# Ejecuta PowerShell como Administrador si instalas para todos los usuarios
Install-Module ExchangeOnlineManagement -Scope AllUsers

# Actualizar
Update-Module ExchangeOnlineManagement
```

> Si recibes errores de repositorio, registra PSGallery:
```powershell
Register-PSRepository -Default
Install-Module PowerShellGet -Force
```

### 2.3 Importar el módulo y comprobar versión cargada
```powershell
Import-Module ExchangeOnlineManagement
Get-Module ExchangeOnlineManagement | Select-Object Name, Version
```

### 2.4 Conectarse a Exchange Online y probar cmdlets
```powershell
# Autenticación interactiva (MFA compatible)
Connect-ExchangeOnline

# Probar con un buzón (requiere permisos)
Get-EXOMailbox -ResultSize 1 | Format-Table DisplayName, UserPrincipalName

# Cerrar sesión
Disconnect-ExchangeOnline
```

---

## 3. Active Directory — módulo `ActiveDirectory`

### 3.1. Verificar si el módulo está disponible
```powershell
Get-Module -ListAvailable ActiveDirectory
```

### 3.2 Importar y probar una consulta básica
```powershell
Import-Module ActiveDirectory

# Buscar por sAMAccountName exacto
Get-ADUser -Identity juan.perez

# Búsqueda parcial por nombre
Get-ADUser -Filter "Name -like '*juan*'" | Select-Object Name, SamAccountName
```

### 3. Instalar el módulo (RSAT) si no está disponible

**Windows 10 (1809+) / Windows 11**:
```powershell
# Windows 11
aDd-WindowsCapability -Online -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0

# Windows 10 (consulta y añade cualquier variante de RSAT AD)
Get-WindowsCapability -Online | Where-Object Name -like 'Rsat.ActiveDirectory*' | Add-WindowsCapability -Online
```

> Requiere acceso a Windows Update o repositorio corporativo (WSUS). Tras instalar:
```powershell
Import-Module ActiveDirectory
Get-Module ActiveDirectory | Select-Object Name, Version
```

---

Cómo resolver el estado InstallPending al instalar RSAT Active Directory
Cuando intentas instalar la característica RSAT Active Directory en Windows y el estado aparece como InstallPending, significa que la instalación no se ha completado. Esto puede deberse a:

Falta reinicio del equipo.
Falta de conectividad a Windows Update o WSUS.
Políticas corporativas que bloquean la instalación.


1. Confirmar el estado actual
Ejecuta:
Get-WindowsCapability -Online | Where-Object Name -like 'Rsat.ActiveDirectory*'


Si el State sigue en InstallPending, la instalación no está lista.
También puedes usar:
DISM /Online /Get-Capabilities | findstr ActiveDirectory




2. Primer paso: reiniciar
Reinicia el equipo y vuelve a ejecutar el comando anterior. Si el estado cambia a Installed, la instalación está completa.


3. Si sigue en InstallPending

Verifica conectividad a Windows Update o WSUS.
Si no hay acceso, solicita a TI el paquete offline RSAT para tu versión exacta de Windows.
Puedes intentar forzar la instalación:
DISM /Online /Add-Capability /CapabilityName:Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0


Si falla, usa el paquete offline:
DISM /Online /Add-Package /PackagePath:"C:\ruta\RSAT.cab"




4. Confirmar instalación
Cuando esté instalado:
Test-Path "C:\Windows\System32\WindowsPowerShell\v1.0\Modules\ActiveDirectory"
Get-Module -ListAvailable ActiveDirectory
Import-Module ActiveDirectory


Si el módulo se importa correctamente, la instalación está completa.


5. Próximos pasos

Si no puedes instalar RSAT, considera usar LDAP con .NET para consultas temporales.
Documenta el proceso y coordina con TI para habilitar la instalación en entornos corporativos.

---

## 4. Selector de archivos para leer CSV de usuarios y buscar en AD

### 4.1 CSV simple (una columna con `sAMAccountName`)
```powershell
Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Title = "Selecciona el archivo de usuarios"
$dialog.Filter = "CSV (*.csv)|*.csv|Texto (*.txt)|*.txt|Todos (*.*)|*.*"
$null = $dialog.ShowDialog()

if ([string]::IsNullOrWhiteSpace($dialog.FileName)) { throw "No se seleccionó archivo." }

$usuarios = Get-Content -Path $dialog.FileName | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }

# Con módulo ActiveDirectory
Import-Module ActiveDirectory
foreach ($sam in $usuarios) {
    $sam = $sam.Trim()
    $u = Get-ADUser -Filter "sAMAccountName -eq '$sam'" -Properties userPrincipalName, mail -ErrorAction SilentlyContinue
    if ($u) {
        Write-Host ("✔ {0} | UPN: {1} | Mail: {2}" -f $u.SamAccountName, $u.UserPrincipalName, $u.Mail) -ForegroundColor Green
    } else {
        Write-Host ("✖ {0} no encontrado" -f $sam) -ForegroundColor Red
    }
}
```
---

## 5. Solución de problemas comunes

- **PSGallery no disponible / políticas corporativas:** usar repositorio interno o instalación offline de RSAT.
- **MFA / errores de conexión a Exchange:** actualizar `ExchangeOnlineManagement` y usar PowerShell 7.x.
- **Sin permisos en AD:** ejecutar PowerShell con una cuenta con privilegios y/o especificar credenciales en `DirectoryEntry`.

---

## 6. Glosario rápido

- **ExchangeOnlineManagement:** módulo para administrar Exchange Online vía PowerShell.
- **RSAT Active Directory:** herramientas de administración remota que incluyen el módulo `ActiveDirectory`.
- **LDAP:** protocolo para acceder y mantener información de directorio.

---

## 8. Pendientes / Próximos pasos

- Añadir validaciones y exportación de resultados a CSV.
- Integrar búsqueda en **Azure AD (Entra ID)** via `Microsoft.Graph` cuando sea directorio cloud-only.
- Documentar parámetros regionales y rutas internas de la agencia.

