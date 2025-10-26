# 🏦 Asesor PyME Inteligente - MCP Financiero

## 📋 Descripción del Proyecto

**Asesor PyME Inteligente** es una solución financiera innovadora que utiliza Model Context Protocol (MCP) para proporcionar análisis financiero inteligente y recomendaciones proactivas a pequeñas y medianas empresas. La solución incluye un asesor financiero virtual con personalidad profesional de Banorte, síntesis de voz con ElevenLabs, análisis avanzado con Snowflake Data Cloud, y está desplegada en Azure usando arquitectura Arm para máxima eficiencia energética.

### 🎯 Objetivos del Reto Banorte

- ✅ Crear un servidor MCP funcional para análisis financiero
- ✅ Desarrollar un frontend intuitivo con dashboard interactivo
- ✅ Implementar simulaciones "What-If" para proyecciones financieras
- ✅ Integrar IA conversacional con Google Gemini
- ✅ Implementar asesor financiero virtual con personalidad profesional
- ✅ Sistema de autenticación empresarial y panel administrativo
- ✅ Gestión completa de datos financieros (CRUD)
- ✅ Desplegar en Azure con arquitectura Arm (premio MLH)

### 🏆 Categorías MLH Competidas

- ✅ **Best Use of Gemini API**: Chat inteligente con Carlos Mendoza
- ✅ **Best Use of Snowflake API**: Análisis financiero avanzado en la nube
- ✅ **Best Use of ElevenLabs**: Síntesis de voz para chat interactivo
- ✅ **Best Use of Arm**: Azure VM con arquitectura Arm
- 🎯 **Best .Tech Domain**: `poweredbymaya.tech`

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│   Azure VM       │◄──►│   Snowflake     │
│   (React)       │    │   (Arm-based)    │    │   Data Cloud   │
│                 │    │                  │    │                 │
│ • Dashboard     │    │ • MCP Server     │    │ • Data Warehouse│
│ • Chat Asesor   │    │ • FastAPI        │    │ • Data Lake     │
│ • Simulaciones  │    │ • Data Analysis  │    │ • ML Functions  │
│ • Gestión Datos │    │ • Auth System    │    │ • Analytics     │
│ • Admin Panel   │    │ • JWT Security   │    │ • Scalability   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AI Services   │
                       │                 │
                       │ • Gemini API    │
                       │ • ElevenLabs    │
                       │ • Voice Synthesis│
                       │ • NLP Analysis  │
                       └─────────────────┘
```

## 🚀 Características Principales

### 👩‍💼 Asesor Financiero Virtual Profesional
- **Maya**: Asesora Financiera de Banorte con experiencia en gestión empresarial
- **Personalidad profesional**: Tono conversacional y directo, como consultor de confianza
- **Enfoque empresarial**: Siempre orientado al crecimiento sostenible de PyMEs
- **Productos Banorte**: Recomendaciones específicas de créditos, inversiones y seguros
- **Análisis profundo**: Respuestas basadas en datos concretos y métricas clave

### 🎤 Chat con Síntesis de Voz (ElevenLabs)
- **Voz natural**: Síntesis de voz profesional para Maya
- **Audio interactivo**: Reproducción de respuestas del asesor
- **Control de audio**: Botones de play/pause en cada mensaje
- **Accesibilidad**: Experiencia inclusiva para usuarios con discapacidades
- **Optimización de créditos**: Texto truncado a 500 caracteres para eficiencia

### 💬 Chat Inteligente Empresarial
- Preguntas en lenguaje natural: *"¿Cómo puedo mejorar mi flujo de caja mensual?"*
- Análisis automático de viabilidad financiera
- Recomendaciones personalizadas basadas en datos históricos
- Sugerencias proactivas de productos bancarios
- Preguntas de seguimiento para profundizar en temas

### 📊 Simulador Financiero "What-If"
- Proyecciones de escenarios futuros
- Análisis de impacto en flujo de caja
- Visualizaciones interactivas de tendencias
- Evaluación de riesgos y oportunidades

### 🏔️ Análisis Avanzado con Snowflake
- **Data Cloud**: Escalabilidad masiva para múltiples PyMEs
- **Análisis histórico**: Tendencias de 12+ meses
- **Simulaciones complejas**: Escenarios con datos reales
- **Métricas avanzadas**: Volatilidad, crecimiento, ROI
- **SQL nativo**: Consultas optimizadas para análisis profundo

### 🔍 Análisis Inteligente
- Detección automática de patrones en gastos
- Identificación de oportunidades de optimización
- Proyecciones de crecimiento basadas en tendencias
- Alertas proactivas sobre riesgos financieros

### 🏢 Gestión Empresarial Completa
- **Autenticación empresarial**: Login por empresa_id para PyMEs
- **Gestión de transacciones**: CRUD completo con datos reales en Snowflake
- **Filtrado por empresa**: Datos específicos por empresa_id
- **Panel administrativo**: Control de accesos y gestión de usuarios
- **Seguridad JWT**: Tokens seguros para ambas interfaces
- **Persistencia en Snowflake**: Todas las transacciones se guardan en la nube

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Google Gemini**: IA conversacional y análisis
- **Snowflake**: Data Cloud para análisis avanzado
- **ElevenLabs**: Síntesis de voz profesional
- **Pandas & Scikit-learn**: Análisis de datos y ML
- **SQLite**: Base de datos local (fallback)
- **JWT**: Autenticación segura
- **Pydantic**: Validación de datos

### Frontend
- **React**: Interfaz de usuario moderna
- **Tailwind CSS**: Estilos con paleta Banorte
- **Framer Motion**: Animaciones fluidas
- **Chart.js**: Visualizaciones financieras
- **Axios**: Comunicación con API
- **React Router**: Navegación SPA
- **Lucide React**: Iconografía moderna

### Infraestructura
- **Azure VM**: Servidor con procesador Arm
- **Snowflake Data Cloud**: Escalabilidad masiva
- **Docker**: Containerización
- **Nginx**: Proxy reverso
- **SSL/TLS**: Seguridad de comunicaciones

## 🎨 Diseño y UX

### Paleta de Colores Banorte
- **Primario**: #EB0029 (Rojo Banorte)
- **Secundario**: #49474 (Gris corporativo)
- **Acento**: #7B868C (Gris iconos)
- **Éxito**: #00AA44 (Verde financiero)
- **Fondo**: #F5F8FA (Gris claro)

### Características de UX
- **Responsive Design**: Adaptable a todos los dispositivos
- **Animaciones suaves**: Transiciones fluidas con Framer Motion
- **Iconografía consistente**: Lucide React para iconos
- **Tipografía profesional**: Inter y Poppins
- **Accesibilidad**: Cumple estándares WCAG

## 🔐 Seguridad y Autenticación

### Sistema Empresarial
- **Login empresarial**: Credenciales específicas para PyMEs
- **JWT Tokens**: Autenticación segura
- **Datos protegidos**: Información financiera encriptada
- **Sesiones persistentes**: LocalStorage seguro

### Panel Administrativo
- **Acceso restringido**: Solo administradores autorizados
- **Gestión de usuarios**: CRUD completo de cuentas
- **Monitoreo**: Último acceso y estadísticas
- **Control de permisos**: Roles y estados de usuario

## 📈 Casos de Uso Demostrados

### 1. Análisis de Viabilidad de Contratación
- **Pregunta**: *"¿Podemos contratar un nuevo empleado el próximo mes?"*
- **Análisis**: Evaluación de flujo de caja, gastos operativos y proyecciones
- **Recomendación**: Respuesta basada en datos reales con alternativas

### 2. Optimización de Gastos
- **Pregunta**: *"¿Dónde puedo reducir gastos sin afectar operaciones?"*
- **Análisis**: Identificación de categorías de gastos optimizables
- **Recomendación**: Estrategias específicas con impacto cuantificado

### 3. Simulación de Expansión
- **Escenario**: Inversión en nueva maquinaria
- **Proyección**: Impacto en flujo de caja a 12 meses
- **Análisis**: ROI y punto de equilibrio

### 4. Gestión de Datos Financieros
- **Funcionalidad**: CRUD completo de transacciones
- **Categorización**: Ingresos y gastos automáticos
- **Reportes**: Análisis en tiempo real

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- Docker (opcional)
- Cuenta Azure (para despliegue)
- Cuenta Snowflake (trial gratuito)
- API Key ElevenLabs

### Instalación Local
```bash
# Clonar repositorio
git clone <repository-url>
cd asesor-financiero

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus API keys

# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

### Configuración de Servicios

#### Snowflake
```bash
# Crear cuenta trial en Snowflake
# Configurar variables en .env:
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password

# Migrar datos
python migrate_to_snowflake.py
```

#### ElevenLabs
```bash
# Obtener API key de ElevenLabs
# Configurar en .env:
ELEVENLABS_API_KEY=your_api_key
```

### Despliegue en Azure (Arquitectura Arm)

#### Deployment Automático (Recomendado)
```bash
# 1. Configurar GitHub Secrets (ver azure/README.md)
# 2. Hacer push a main
# 3. El deployment se ejecuta automáticamente
```

#### Deployment Manual
```bash
# Usar script de despliegue
chmod +x azure/deploy.sh
./azure/deploy.sh
```

**Ver [azure/README.md](azure/README.md) para instrucciones completas de deployment.**

## 📊 API Endpoints

### Análisis Financiero
- `GET /api/analysis/profitability` - Análisis de rentabilidad
- `GET /api/analysis/cashflow` - Análisis de flujo de caja
- `GET /api/analysis/expenses` - Análisis de gastos
- `GET /api/analysis/revenue` - Análisis de ingresos

### Chat Inteligente
- `POST /api/chat/message` - Enviar mensaje al asesor
- `POST /api/chat/audio` - Generar respuesta de audio
- `GET /api/chat/suggestions` - Obtener sugerencias de preguntas
- `GET /api/chat/voices` - Obtener voces disponibles
- `GET /api/chat/history` - Historial de conversación

### Simulaciones
- `POST /api/simulations/scenario` - Crear nuevo escenario
- `GET /api/simulations/history` - Historial de simulaciones
- `GET /api/simulations/{id}` - Obtener simulación específica

### Gestión de Transacciones
- `GET /api/transactions/` - Listar últimas transacciones (filtrar por empresa)
- `POST /api/transactions/` - Crear nueva transacción en Snowflake
- `DELETE /api/transactions/{id}` - Eliminar transacción
- **Header requerido**: `X-Empresa-ID` para filtrar datos por empresa

### Snowflake Integration
- `GET /api/snowflake/analysis` - Análisis avanzado con Snowflake
- `POST /api/snowflake/simulation` - Simulación con datos históricos
- `GET /api/snowflake/metrics` - Métricas calculadas automáticamente

## 🎥 Demo Video

**Duración**: 5 minutos
**Estructura sugerida**:
1. **Introducción** (30s): Problema y solución innovadora
2. **Demo del Asesor con Audio** (2m): Chat con Carlos Mendoza + síntesis de voz
3. **Análisis con Snowflake** (1m): Tendencias históricas y métricas avanzadas
4. **Simulaciones** (1m): Escenarios What-If con datos reales
5. **Dashboard** (30s): Métricas en tiempo real
6. **Gestión de Datos** (30s): CRUD de transacciones
7. **Panel Admin** (30s): Control de accesos
8. **Conclusión** (30s): Beneficios y próximos pasos

## 🏆 Premios y Reconocimientos

### Hack Mty 2025
- **Reto Banorte**: Solución financiera innovadora
- **Premio MLH Arm**: Arquitectura eficiente energéticamente
- **Innovación**: MCP + IA conversacional profesional + Audio + Cloud

### Categorías MLH Competidas
- ✅ **Best Use of Gemini API**: Chat inteligente con personalidad profesional
- ✅ **Best Use of Snowflake API**: Análisis financiero avanzado en la nube
- ✅ **Best Use of ElevenLabs**: Síntesis de voz para chat interactivo
- ✅ **Best Use of Arm**: Azure VM con arquitectura Arm
- 🎯 **Best .Tech Domain**: `poweredbymaya.tech`

### Criterios de Evaluación
- ✅ **Funcionalidad**: Sistema completo y operativo
- ✅ **Innovación**: Asesor virtual con personalidad + audio + cloud
- ✅ **Impacto**: Solución real para PyMEs
- ✅ **Técnica**: Arquitectura moderna y escalable
- ✅ **Presentación**: Demo profesional y documentación completa

## 👥 Equipo *Migajeros*

- *Vanessa Nohely Arrambide Escamilla* (UANL) (Licenciatura en Tecnologías de la Información)
- *Rebeca Aylen Martinez Guajardo* (Tecmilenio) (Ingeniaría en Desarrollador de Software)
- *Guillermo Rigoberto De Anda López* (Tecmilenio) (Ingeniaría en Desarrollador de Software)
- *Edgar Omar Najera Vazquez* (UANL) (Licenciatura en Tecnologías de la Información)

## 📄 Licencia

Este proyecto está desarrollado para el Hack Mty 2025 y el Reto Banorte. Todos los derechos reservados.

## 🤝 Contribuciones

Este proyecto fue desarrollado específicamente para el Hack Mty 2025. Para consultas o colaboraciones futuras, contactar al equipo de desarrollo.

---

## 🙏 Agradecimientos

Queremos expresar nuestro más sincero agradecimiento a todas las instituciones y organizaciones que hicieron posible esta increíble experiencia:

- **Tecnológico de Monterrey** - Por su liderazgo en innovación tecnológica y por organizar este magno evento.

### 🎯 **Organizadores del Evento**
- **HACKMty** - Por crear un espacio único donde la innovación y la tecnología se encuentran.
- **Tec ACM** - Por promover el crecimiento de los estudiantes y llevar a cabo este gran evento.

### 🏦 **Patrocinadores**
- **Banorte** - Por el reto inspirador que nos permitió desarrollar una solución financiera innovadora
- **Todos los patrocinadores** - Por su invaluable apoyo que hace posible eventos de esta magnitud.

### 💡 **Reconocimiento Especial**
Este proyecto representa más que una solución técnica; es el resultado de la colaboración, el aprendizaje continuo y la pasión por crear tecnología que genere impacto real en la sociedad. La oportunidad de participar en HACKMty nos ha permitido:

- Desarrollar habilidades técnicas avanzadas
- Trabajar en equipo bajo presión
- Crear soluciones innovadoras para problemas reales
- Conectar con la comunidad tecnológica de México
- Contribuir al ecosistema de innovación financiera

### 🚀 **Compromiso Futuro**
Como equipo *Migajeros*, nos comprometemos a continuar desarrollando tecnología que transforme la manera en que las PyMEs gestionan sus finanzas, siempre con el objetivo de democratizar el acceso a herramientas financieras avanzadas.

**¡Gracias por creer en el potencial de los estudiantes y por impulsar la innovación tecnológica en México!**

---

**🏦 Asesor PyME Inteligente** - *Transformando la asesoría financiera con IA, voz y cloud*

### 🌐 Dominio Recomendado
**`poweredbymaya.tech`** - Plataforma profesional para PyMEs

### 📚 Documentación Adicional
- [SNOWFLAKE_INTEGRATION.md](SNOWFLAKE_INTEGRATION.md) - Guía completa de integración con Snowflake
- [DOMAIN_STRATEGY.md](DOMAIN_STRATEGY.md) - Estrategia de dominio .tech
- [DEMO.md](DEMO.md) - Guía de demostración
- [INSTALLATION.md](INSTALLATION.md) - Instrucciones detalladas de instalación