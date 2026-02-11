# 🐉 Kali Linux – Mantenimiento, Actualización y Limpieza

:leftwards_arrow_with_hook: [python-cybersecurity-tools](../README.md)


Guía práctica para mantener **Kali Linux (kali-rolling)** limpio, estable y actualizado.

---

## 🔄 Actualización del Sistema

### Actualizar listas de repositorios
```bash
sudo apt update
```

### Ver paquetes actualizables
```bash
apt list --upgradable
```

### Actualizar el sistema (recomendado)
```bash
sudo apt full-upgrade
```

---

## 🧹 Limpieza de Paquetes y Caché

### Eliminar dependencias innecesarias
```bash
sudo apt autoremove
```

### Eliminar dependencias y configuraciones
```bash
sudo apt autoremove --purge
```

### Limpiar todo el caché
```bash
sudo apt clean
```

### Limpiar solo paquetes obsoletos del caché
```bash
sudo apt autoclean
```

---

## 🗑️ Paquetes Obsoletos

### Ver paquetes obsoletos
```bash
apt list '~o'
```

### Eliminar paquetes obsoletos específicos
```bash
sudo apt purge paquete1 paquete2
```

### Eliminar TODOS los obsoletos (riesgo)
```bash
sudo apt purge '~o'
```

⚠️ No ejecutar sin revisar kernel y drivers.

---

## 🧾 Repositorios

### Ver repositorios activos
```bash
cat /etc/apt/sources.list
```

### Buscar repos duplicados
```bash
grep -R http /etc/apt/sources.list /etc/apt/sources.list.d/
```

### Limpiar listas viejas de repos
```bash
sudo rm -rf /var/lib/apt/lists/*
sudo apt update
```

---

## 🛠️ Reparación

```bash
sudo apt --fix-broken install
sudo dpkg --configure -a
```

---

## 🧠 Comprobaciones Importantes

### Kernel en uso
```bash
uname -r
```

### Kernels instalados
```bash
dpkg --list | grep linux-image
```

---

## 🖥️ Problema: Letras extrañas o símbolos raros en el menú

### Síntomas
- Texto corrupto
- Caracteres raros en menús
- Fuentes ilegibles

### Solución (comprobada)
```bash
sudo fc-cache -fv
```

Cerrar sesión o reiniciar.

### Causa
Caché de fuentes corrupta tras actualizaciones o cambios gráficos.

---

## 🚀 Secuencia Recomendada

```bash
sudo apt update &&
sudo apt full-upgrade &&
sudo apt autoremove --purge &&
sudo apt clean
```

---

## ⚠️ Reglas de Oro en Kali

- No mezclar repos Debian/Ubuntu
- No usar PPAs
- No borrar kernels sin verificar
- No usar optimizadores

---

✔ Documento listo para Git / Wiki / Notas técnicas
