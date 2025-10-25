# 🏦 Asesor PyME Inteligente - MCP Financiero

## 📋 Descripción del Proyecto

**Asesor PyME Inteligente** es una solución financiera innovadora que utiliza Model Context Protocol (MCP) para proporcionar análisis financiero inteligente y recomendaciones proactivas a pequeñas y medianas empresas. La solución incluye un asesor financiero virtual con personalidad profesional de Banorte y está desplegada en Azure usando arquitectura Arm para máxima eficiencia energética.

### 🎯 Objetivos del Reto Banorte

- ✅ Crear un servidor MCP funcional para análisis financiero
- ✅ Desarrollar un frontend intuitivo con dashboard interactivo
- ✅ Implementar simulaciones "What-If" para proyecciones financieras
- ✅ Integrar IA conversacional con Google Gemini
- ✅ Implementar asesor financiero virtual con personalidad profesional
- ✅ Sistema de autenticación empresarial y panel administrativo
- ✅ Gestión completa de datos financieros (CRUD)
- ✅ Desplegar en Azure con arquitectura Arm (premio MLH)

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Azure VM       │    │   Google        │
│   (React)       │◄──►│   (Arm-based)    │◄──►│   Gemini API    │
│                 │    │                  │    │                 │
│ • Dashboard     │    │ • MCP Server     │    │ • NLP           │
│ • Chat Asesor   │    │ • FastAPI        │    │ • Analysis      │
│ • Simulaciones  │    │ • Data Analysis  │    │ • Recommendations│
│ • Gestión Datos │    │ • Auth System    │    │ • Professional   │
│ • Admin Panel   │    │ • JWT Security   │    │   Personality   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Data Sources  │
                       │                 │
                       │ • Excel Files   │
                       │ • SQLite DB     │
                       │ • User Data     │
                       │ • Transactions  │
                       └─────────────────┘
```

## 🚀 Características Principales

### 👨‍💼 Asesor Financiero Virtual Profesional
- **Carlos Mendoza**: Asesor Financiero Senior de Banorte con 15+ años de experiencia
- **Personalidad profesional**: Tono cercano pero experto, como consultor de confianza
- **Enfoque empresarial**: Siempre orientado al crecimiento sostenible de PyMEs
- **Productos Banorte**: Recomendaciones específicas de créditos, inversiones y seguros
- **Análisis profundo**: Respuestas basadas en datos concretos y métricas clave

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

### 🔍 Análisis Inteligente
- Detección automática de patrones en gastos
- Identificación de oportunidades de optimización
- Proyecciones de crecimiento basadas en tendencias
- Alertas proactivas sobre riesgos financieros

### 🏢 Gestión Empresarial Completa
- **Autenticación empresarial**: Login seguro para PyMEs
- **Gestión de datos**: CRUD completo de transacciones financieras
- **Panel administrativo**: Control de accesos y gestión de usuarios
- **Seguridad JWT**: Tokens seguros para ambas interfaces

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Google Gemini**: IA conversacional y análisis
- **Pandas & Scikit-learn**: Análisis de datos y ML
- **SQLite**: Base de datos local
- **JWT**: Autenticación segura
- **Pydantic**: Validación de datos

### Frontend
- **React**: Interfaz de usuario moderna
- **Tailwind CSS**: Estilos con paleta Banorte
- **Framer Motion**: Animaciones fluidas
- **Chart.js**: Visualizaciones financieras
- **Axios**: Comunicación con API
- **React Router**: Navegación SPA

### Infraestructura
- **Azure VM**: Servidor con procesador Arm
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

### Instalación Local
```bash
# Clonar repositorio
git clone <repository-url>
cd asesor-financiero

# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

### Despliegue en Azure
```bash
# Usar script de despliegue
chmod +x azure/deploy.sh
./azure/deploy.sh
```

## 📊 API Endpoints

### Análisis Financiero
- `GET /api/analysis/profitability` - Análisis de rentabilidad
- `GET /api/analysis/cashflow` - Análisis de flujo de caja
- `GET /api/analysis/expenses` - Análisis de gastos
- `GET /api/analysis/revenue` - Análisis de ingresos

### Chat Inteligente
- `POST /api/chat/message` - Enviar mensaje al asesor
- `GET /api/chat/suggestions` - Obtener sugerencias de preguntas
- `GET /api/chat/history` - Historial de conversación

### Simulaciones
- `POST /api/simulations/scenario` - Crear nuevo escenario
- `GET /api/simulations/history` - Historial de simulaciones
- `GET /api/simulations/{id}` - Obtener simulación específica

### Gestión de Datos
- `GET /api/data/transactions` - Listar transacciones
- `POST /api/data/transactions` - Crear transacción
- `PUT /api/data/transactions/{id}` - Actualizar transacción
- `DELETE /api/data/transactions/{id}` - Eliminar transacción

## 🎥 Demo Video

**Duración**: 5 minutos
**Estructura sugerida**:
1. **Introducción** (30s): Problema y solución
2. **Demo del Asesor** (2m): Chat con Carlos Mendoza
3. **Simulaciones** (1m): Escenarios What-If
4. **Dashboard** (1m): Métricas y análisis
5. **Gestión de Datos** (30s): CRUD de transacciones
6. **Panel Admin** (30s): Control de accesos
7. **Conclusión** (30s): Beneficios y próximos pasos

## 🏆 Premios y Reconocimientos

### Hack Mty 2025
- **Reto Banorte**: Solución financiera innovadora
- **Premio MLH Arm**: Arquitectura eficiente energéticamente
- **Innovación**: MCP + IA conversacional profesional

### Criterios de Evaluación
- ✅ **Funcionalidad**: Sistema completo y operativo
- ✅ **Innovación**: Asesor virtual con personalidad profesional
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

**🏦 Asesor PyME Inteligente** - *Transformando la asesoría financiera con IA*