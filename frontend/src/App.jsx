import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard, Map, ScanSearch, Waves, Database,
  Bell, Search, ChevronDown, Leaf, Activity, AlertTriangle,
  ArrowUpRight, TrendingUp, Layers, Microscope,
  Satellite, ShieldCheck, CircleDot, FlaskConical
} from "lucide-react";
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from "recharts";
import "./App.css";

// Dashboard navigation
const navigation = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "GIS Monitoring", icon: Map },
  { name: "Disease Detection", icon: ScanSearch },
  { name: "Spectral Analysis", icon: Waves },
  { name: "Dataset Explorer", icon: Database },
];

// Illustrative spectral data
const spectralData = [
  { band: "450", healthy: 28, stressed: 36 },
  { band: "500", healthy: 35, stressed: 41 },
  { band: "550", healthy: 43, stressed: 46 },
  { band: "600", healthy: 39, stressed: 52 },
  { band: "650", healthy: 48, stressed: 57 },
  { band: "700", healthy: 72, stressed: 61 },
  { band: "750", healthy: 88, stressed: 66 },
  { band: "800", healthy: 94, stressed: 69 },
  { band: "850", healthy: 91, stressed: 65 },
];

// Illustrative crop health distribution
const healthData = [
  { name: "Healthy", value: 68, color: "#55d99a" },
  { name: "Stressed", value: 22, color: "#e8b45c" },
  { name: "Critical", value: 10, color: "#ed7474" },
];

// Illustrative dashboard metrics
const stats = [
  {
    label: "Monitored Fields",
    value: "128",
    change: "+12.8%",
    icon: Layers,
    color: "green"
  },
  {
    label: "Crop Health Index",
    value: "94.2%",
    change: "+4.6%",
    icon: Leaf,
    color: "mint"
  },
  {
    label: "Disease Alerts",
    value: "08",
    change: "2 high priority",
    icon: AlertTriangle,
    color: "orange"
  },
  {
    label: "Data Processed",
    value: "2.4 TB",
    change: "+18.3%",
    icon: Database,
    color: "blue"
  },
];

// OVERVIEW PAGE
function Overview() {
  return (
    <>
      <div className="welcome-row">
        <div>
          <p className="eyebrow">INTELLIGENCE OVERVIEW</p>
          <h1>Good evening, <span>Researcher.</span></h1>
          <p className="subtitle">
            Here's what's happening across your agricultural ecosystem.
          </p>
        </div>

        <div className="date-pill">
          <CircleDot size={13} />
          LIVE MONITORING
          <span className="live-dot" />
        </div>
      </div>

      <div className="stats-grid">
        {stats.map((stat, i) => {
          const Icon = stat.icon;

          return (
            <motion.div
              className="stat-card"
              key={stat.label}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
            >
              <div className="stat-top">
                <span>{stat.label}</span>
                <div className={`stat-icon ${stat.color}`}>
                  <Icon size={19} />
                </div>
              </div>

              <div className="stat-value">{stat.value}</div>

              <div className="stat-change">
                <TrendingUp size={13} />
                {stat.change}
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="dashboard-grid">
        <section className="panel spectral-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">REMOTE SENSING</p>
              <h2>Spectral Signature Analysis</h2>
            </div>
            <span className="panel-tag">ILLUSTRATIVE DATA</span>
          </div>

          <p className="panel-description">
            Example reflectance curves for healthy and stressed crop vegetation.
          </p>

          <div className="chart-legend">
            <span>
              <i className="legend-dot healthy-dot" />
              Healthy vegetation
            </span>
            <span>
              <i className="legend-dot stressed-dot" />
              Stressed vegetation
            </span>
          </div>

          <div className="chart-area">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={spectralData}>
                <defs>
                  <linearGradient
                    id="healthyFill"
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop
                      offset="0%"
                      stopColor="#55d99a"
                      stopOpacity={0.25}
                    />
                    <stop
                      offset="100%"
                      stopColor="#55d99a"
                      stopOpacity={0}
                    />
                  </linearGradient>
                </defs>

                <CartesianGrid
                  stroke="#25362e"
                  strokeDasharray="3 5"
                  vertical={false}
                />

                <XAxis
                  dataKey="band"
                  stroke="#789083"
                  tick={{ fontSize: 11 }}
                />

                <YAxis
                  stroke="#789083"
                  tick={{ fontSize: 11 }}
                />

                <Tooltip
                  contentStyle={{
                    background: "#14221b",
                    border: "1px solid #30493a",
                    borderRadius: 10
                  }}
                />

                <Area
                  type="monotone"
                  dataKey="healthy"
                  stroke="#55d99a"
                  fill="url(#healthyFill)"
                  strokeWidth={2.5}
                />

                <Area
                  type="monotone"
                  dataKey="stressed"
                  stroke="#e8b45c"
                  fill="none"
                  strokeWidth={2.5}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-footer">
            Wavelength (nm)
            <span>Illustrative reflectance values</span>
          </div>
        </section>

        <section className="panel health-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">FIELD DISTRIBUTION</p>
              <h2>Crop Health Status</h2>
            </div>
            <span className="more-icon">
              <ArrowUpRight size={17} />
            </span>
          </div>

          <p className="panel-description">
            Example distribution across monitored fields.
          </p>

          <div className="donut-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={healthData}
                  dataKey="value"
                  innerRadius={67}
                  outerRadius={91}
                  paddingAngle={5}
                  stroke="none"
                >
                  {healthData.map((entry) => (
                    <Cell
                      key={entry.name}
                      fill={entry.color}
                    />
                  ))}
                </Pie>

                <Tooltip
                  contentStyle={{
                    background: "#14221b",
                    border: "1px solid #30493a",
                    borderRadius: 10
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            <div className="donut-center">
              <strong>68%</strong>
              <span>HEALTHY</span>
            </div>
          </div>

          <div className="health-legend">
            {healthData.map(item => (
              <div key={item.name}>
                <span>
                  <i style={{ background: item.color }} />
                  {item.name}
                </span>
                <strong>{item.value}%</strong>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="panel activity-panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">SYSTEM ACTIVITY</p>
            <h2>Recent Intelligence Updates</h2>
          </div>
          <span className="panel-tag">SAMPLE FEED</span>
        </div>

        <div className="activity-item">
          <span className="activity-icon green">
            <Leaf size={17} />
          </span>
          <div>
            <strong>Crop health scan completed</strong>
            <p>Sample field monitoring event</p>
          </div>
          <time>Recently</time>
        </div>

        <div className="activity-item">
          <span className="activity-icon orange">
            <AlertTriangle size={17} />
          </span>
          <div>
            <strong>Illustrative disease alert</strong>
            <p>Example alert for interface preview</p>
          </div>
          <time>Recently</time>
        </div>

        <div className="activity-item">
          <span className="activity-icon blue">
            <Satellite size={17} />
          </span>
          <div>
            <strong>Remote sensing data updated</strong>
            <p>Sample satellite data activity</p>
          </div>
          <time>Recently</time>
        </div>
      </section>

      <p className="demo-note">
        Dashboard preview · Metrics and charts shown are illustrative demo data,
        not validated model predictions.
      </p>
    </>
  );
}

// REUSABLE SECTION LAYOUT
function SectionPage({
  title,
  eyebrow,
  description,
  icon: Icon,
  children
}) {
  return (
    <motion.div
      className="section-page"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="welcome-row">
        <div>
          <p className="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p className="subtitle">{description}</p>
        </div>

        <div className="section-hero-icon">
          <Icon size={30} />
        </div>
      </div>

      {children}
    </motion.div>
  );
}

// GIS MONITORING PAGE
function GISPage() {
  return (
    <SectionPage
      title="Geospatial Monitoring"
      eyebrow="SPATIAL INTELLIGENCE"
      description="Explore agricultural field locations and monitoring layers."
      icon={Map}
    >
      <div className="panel feature-panel">
        <div className="feature-visual map-visual">
          <div className="map-grid">
            <span className="map-pin pin-one" />
            <span className="map-pin pin-two" />
            <span className="map-pin pin-three" />
            <span className="map-pin pin-four" />
            <div className="map-orbit" />
          </div>

          <div className="map-overlay">
            <Satellite size={18} />
            GIS MAP PREVIEW
          </div>
        </div>

        <h2>Field Mapping Workspace</h2>

        <p className="panel-description">
          This is a visual placeholder. Live maps, field coordinates,
          and satellite overlays will be integrated with the GIS module.
        </p>

        <div className="feature-chips">
          <span>Field boundaries</span>
          <span>Satellite layers</span>
          <span>GPS coordinates</span>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span>Mapping status</span>
          <div className="stat-value small-value">UI Preview</div>
        </div>

        <div className="stat-card">
          <span>Map provider</span>
          <div className="stat-value small-value">Integration pending</div>
        </div>
      </div>
    </SectionPage>
  );
}

// DISEASE DETECTION PAGE
function DiseasePage() {
  return (
    <SectionPage
      title="Disease Detection Center"
      eyebrow="AI DIAGNOSTICS"
      description="A workspace for crop disease screening and model-generated alerts."
      icon={ScanSearch}
    >
      <div className="feature-grid">
        <div className="panel feature-panel">
          <div className="large-feature-icon">
            <Microscope size={32} />
          </div>

          <h2>Image & Cube Analysis</h2>

          <p className="panel-description">
            The future detection workflow will accept crop imagery
            or hyperspectral data for model analysis.
          </p>

          <span className="status-chip">
            Model integration pending
          </span>
        </div>

        <div className="panel feature-panel">
          <div className="large-feature-icon warning">
            <ShieldCheck size={32} />
          </div>

          <h2>Diagnostic Reports</h2>

          <p className="panel-description">
            Disease classifications, confidence scores, and validation
            details will appear here when the ML pipeline is connected.
          </p>

          <span className="status-chip">
            Awaiting ML pipeline
          </span>
        </div>
      </div>
    </SectionPage>
  );
}

// SPECTRAL ANALYSIS PAGE
function SpectralPage() {
  return (
    <SectionPage
      title="Spectral Laboratory"
      eyebrow="HYPERSPECTRAL INTELLIGENCE"
      description="Explore wavelength signatures and vegetation reflectance patterns."
      icon={Waves}
    >
      <div className="panel spectral-panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">SPECTRAL EXPLORER</p>
            <h2>Vegetation Reflectance</h2>
          </div>
          <span className="panel-tag">ILLUSTRATIVE</span>
        </div>

        <p className="panel-description">
          Example healthy and stressed crop signatures across
          visible and near-infrared bands.
        </p>

        <div className="chart-legend">
          <span>
            <i className="legend-dot healthy-dot" />
            Healthy
          </span>
          <span>
            <i className="legend-dot stressed-dot" />
            Stressed
          </span>
        </div>

        <div className="large-chart">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={spectralData}>
              <CartesianGrid
                stroke="#25362e"
                strokeDasharray="3 5"
              />

              <XAxis dataKey="band" stroke="#789083" />
              <YAxis stroke="#789083" />

              <Tooltip
                contentStyle={{
                  background: "#14221b",
                  border: "1px solid #30493a",
                  borderRadius: 10
                }}
              />

              <Area
                type="monotone"
                dataKey="healthy"
                stroke="#55d99a"
                fill="#55d99a"
                fillOpacity={0.12}
                strokeWidth={3}
              />

              <Area
                type="monotone"
                dataKey="stressed"
                stroke="#e8b45c"
                fill="#e8b45c"
                fillOpacity={0.08}
                strokeWidth={3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="demo-note">
          Illustrative data only. Real spectral signatures will come
          from the validated dataset and preprocessing pipeline.
        </div>
      </div>

      <div className="feature-grid">
        <div className="stat-card">
          <span>Visible spectrum</span>
          <div className="stat-value small-value">400–700 nm</div>
        </div>

        <div className="stat-card">
          <span>Near-infrared</span>
          <div className="stat-value small-value">700–1000 nm</div>
        </div>
      </div>
    </SectionPage>
  );
}

// DATASET EXPLORER PAGE
function DatasetPage({ datasetInfo, datasetStatus }) {
  const dataset = datasetInfo?.dataset;

  const classEntries = dataset?.class_distribution
    ? Object.entries(dataset.class_distribution)
    : [];

  return (
    <SectionPage
      title="Dataset Explorer"
      eyebrow="DATA INTELLIGENCE"
      description="Explore the connected hyperspectral dataset, its dimensions, and class distribution."
      icon={Database}
    >
      <div className="feature-grid">
        <div className="panel feature-panel">
          <div className="large-feature-icon">
            <Database size={32} />
          </div>

          <h2>Dataset Registry</h2>

          <p className="panel-description">
            Live metadata retrieved from the TerraSpectra FastAPI backend.
          </p>

          <span className="status-chip">
            {datasetStatus === "connected"
              ? "Dataset connected"
              : datasetStatus === "loading"
                ? "Loading dataset information"
                : "Dataset connection unavailable"}
          </span>
        </div>

        <div className="panel feature-panel">
          <div className="large-feature-icon">
            <FlaskConical size={32} />
          </div>

          <h2>Quality & Validation</h2>

          <p className="panel-description">
            Dataset dimensions, label counts, and class distribution are read
            from the dataset metadata endpoint. Model validation is a separate
            step and is not represented by these metadata values.
          </p>

          <span className="status-chip">
            {dataset ? "Metadata retrieved" : "Awaiting dataset metadata"}
          </span>
        </div>
      </div>

      <div className="panel table-panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">DATA INVENTORY</p>
            <h2>Connected dataset information</h2>
          </div>

          <span className="panel-tag">
            {datasetStatus === "connected" ? "LIVE API DATA" : "API STATUS"}
          </span>
        </div>

        {datasetStatus === "loading" && (
          <div className="empty-state">
            <Database size={30} />
            <strong>Loading dataset information...</strong>
            <p>Contacting the TerraSpectra backend.</p>
          </div>
        )}

        {datasetStatus === "error" && (
          <div className="empty-state">
            <AlertTriangle size={30} />
            <strong>Could not load dataset information</strong>
            <p>
              Make sure the FastAPI backend is running and refresh the page.
            </p>
          </div>
        )}

        {dataset && (
          <>
            <div className="stats-grid" style={{ marginTop: "20px" }}>
              <div className="stat-card">
                <span>Total samples</span>
                <div className="stat-value">
                  {dataset.total_samples}
                </div>
              </div>

              <div className="stat-card">
                <span>Image dimensions</span>
                <div className="stat-value small-value">
                  {dataset.image_height} × {dataset.image_width}
                </div>
              </div>

              <div className="stat-card">
                <span>Spectral bands</span>
                <div className="stat-value">
                  {dataset.spectral_bands}
                </div>
              </div>

              <div className="stat-card">
                <span>Classes</span>
                <div className="stat-value">
                  {Object.keys(dataset.classes || {}).length}
                </div>
              </div>
            </div>

            <div style={{ marginTop: "28px" }}>
              <div className="panel-heading">
                <div>
                  <p className="eyebrow">LABEL OVERVIEW</p>
                  <h2>Crop-health class distribution</h2>
                </div>
              </div>

              <div style={{
                display: "grid",
                gap: "14px",
                marginTop: "18px"
              }}>
                {classEntries.map(([className, count]) => {
                  const percentage = dataset.total_samples
                    ? (count / dataset.total_samples) * 100
                    : 0;

                  return (
                    <div key={className}>
                      <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: "12px",
                        marginBottom: "7px",
                        fontSize: "13px"
                      }}>
                        <strong style={{ textTransform: "capitalize" }}>
                          {className.replace(/_/g, " ")}
                        </strong>

                        <span>
                          {count} samples ({percentage.toFixed(1)}%)
                        </span>
                      </div>

                      <div style={{
                        height: "9px",
                        borderRadius: "20px",
                        background: "rgba(130, 160, 140, 0.16)",
                        overflow: "hidden"
                      }}>
                        <div style={{
                          width: `${percentage}%`,
                          height: "100%",
                          borderRadius: "20px",
                          background: "linear-gradient(90deg, #55d99a, #8be0b5)"
                        }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="feature-chips" style={{ marginTop: "24px" }}>
              <span>Labels: {dataset.labels_count}</span>
              <span>Wavelength values: {dataset.wavelength_count}</span>
              <span>Format: HDF5</span>
            </div>
          </>
        )}
      </div>

      <p className="demo-note">
        Dataset metadata is retrieved from the connected local backend.
        The supplied dataset is synthetic and does not establish
        real-world disease-detection accuracy.
      </p>
    </SectionPage>
  );
}

// MAIN APPLICATION
function App() {
  const [active, setActive] = useState("Overview");
  const [search, setSearch] = useState("");

  // Dashboard API state
  const [backendSummary, setBackendSummary] = useState(null);
  const [apiStatus, setApiStatus] = useState("loading");

  // Dataset API state
  const [datasetInfo, setDatasetInfo] = useState(null);
  const [datasetStatus, setDatasetStatus] = useState("loading");

  // Fetch dashboard information
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/dashboard/summary")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend request failed");
        }

        return response.json();
      })
      .then((data) => {
        setBackendSummary(data);
        setApiStatus("connected");
      })
      .catch((error) => {
        console.error("API connection error:", error);
        setApiStatus("error");
      });
  }, []);

  // Fetch actual dataset metadata from FastAPI
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/dataset/info")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Dataset API request failed");
        }

        return response.json();
      })
      .then((data) => {
        setDatasetInfo(data);
        setDatasetStatus("connected");
      })
      .catch((error) => {
        console.error("Dataset API connection error:", error);
        setDatasetStatus("error");
      });
  }, []);

  // Page navigation
  const pageMap = {
    "Overview": <Overview />,
    "GIS Monitoring": <GISPage />,
    "Disease Detection": <DiseasePage />,
    "Spectral Analysis": <SpectralPage />,
    "Dataset Explorer": (
      <DatasetPage
        datasetInfo={datasetInfo}
        datasetStatus={datasetStatus}
      />
    )
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Leaf size={23} />
          </div>

          <div>
            <strong>Terra<span>Spectra</span></strong>
            <small>AGRICULTURAL INTELLIGENCE</small>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav>
          {navigation.map(item => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${active === item.name ? "active" : ""}`}
                onClick={() => setActive(item.name)}
              >
                <Icon size={18} />
                <span>{item.name}</span>

                {active === item.name && (
                  <motion.i layoutId="nav-indicator" />
                )}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="live-dot" />
            SYSTEM ONLINE
          </div>

          <div className="profile">
            <div className="avatar">TS</div>

            <div>
              <strong>Research Workspace</strong>
              <small>Project dashboard</small>
            </div>

            <ChevronDown size={15} />
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            TerraSpectra <span>/</span> <strong>{active}</strong>
          </div>

          <div className="top-actions">
            <div className="search-box">
              <Search size={16} />

              <input
                placeholder="Search workspace..."
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </div>

            <button className="icon-button" aria-label="Notifications">
              <Bell size={18} />
              <i />
            </button>

            <div className="top-avatar">TS</div>
          </div>
        </header>

        <div className="content-area">

          {/* BACKEND CONNECTION PANEL */}
          <div
            style={{
              background: "rgba(80, 180, 110, 0.08)",
              border: "1px solid rgba(100, 190, 130, 0.25)",
              borderRadius: "12px",
              padding: "14px 18px",
              marginBottom: "20px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "12px"
            }}
          >
            <div>
              <strong style={{ fontSize: "14px" }}>
                Backend API Connection
              </strong>

              <div style={{
                fontSize: "12px",
                opacity: 0.75,
                marginTop: "5px"
              }}>
                {apiStatus === "loading" &&
                  "Connecting to TerraSpectra API..."}

                {apiStatus === "connected" &&
                  "Live data received successfully"}

                {apiStatus === "error" &&
                  "Backend connection failed. Check your server."}
              </div>
            </div>

            <div style={{
              fontSize: "12px",
              fontWeight: "600",
              color:
                apiStatus === "connected"
                  ? "#65d995"
                  : apiStatus === "error"
                    ? "#ff7777"
                    : "#e6bb65"
            }}>
              {apiStatus === "connected" && "● CONNECTED"}
              {apiStatus === "loading" && "● CONNECTING"}
              {apiStatus === "error" && "● DISCONNECTED"}
            </div>

            {backendSummary && (
              <div style={{
                width: "100%",
                display: "flex",
                gap: "25px",
                flexWrap: "wrap",
                fontSize: "12px",
                opacity: 0.85
              }}>
                <span>
                  Dataset: {backendSummary.dataset_status}
                </span>

                <span>
                  Model: {backendSummary.model_status}
                </span>

                <span>
                  Samples: {backendSummary.total_samples}
                </span>
              </div>
            )}
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={active}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -5 }}
              transition={{ duration: 0.2 }}
            >
              {pageMap[active]}
            </motion.div>
          </AnimatePresence>
        </div>

        <footer className="footer">
          <span>
            © 2026 TerraSpectra · Hyperspectral Crop Intelligence
          </span>

          <span>
            Research prototype · Demo interface
          </span>
        </footer>
      </main>
    </div>
  );
}

export default App;