import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Users,
    Zap,
    Activity,
    ArrowRight,
    FileText,
    Inbox,
    Package,
    AlertTriangle,
    ShieldCheck,
    Plus,
    CheckCircle,
    X
} from 'lucide-react';

const Dashboard = () => {
    const { user } = useAuth();
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeActionModal, setActiveActionModal] = useState(null);
    const [actionLoading, setActionLoading] = useState(false);

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = () => {
        setLoading(true);
        fetch('/api/aquacycle/dashboard')
            .then(res => res.json())
            .then(res => {
                if (res.status === 'success') {
                    setDashboardData(res.data);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error("Dashboard Fetch Error:", err);
                setLoading(false);
            });
    };

    const handleActionSubmit = (e) => {
        e.preventDefault();
        setActionLoading(true);
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        data.action = activeActionModal;

        fetch('/api/aquacycle/work', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(res => {
                if (res.status === 'success') {
                    alert(res.message);
                    setActiveActionModal(null);
                    fetchDashboard();
                } else {
                    alert(res.message);
                }
                setActionLoading(false);
            })
            .catch(err => {
                console.error("Action Error:", err);
                setActionLoading(false);
            });
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
            </div>
        );
    }

    if (!dashboardData) {
        return (
            <div className="text-center py-20">
                <h2 className="text-2xl font-bold text-white mb-4">Please login to access your portal</h2>
                <a href="/login" className="premium-btn inline-block">Login Now</a>
            </div>
        );
    }

    const { role_info, connections, leads, reports, widgets, recent_activity, user_info } = dashboardData;

    // Define role-based available actions
    const roleActions = {
        hatchery_owner: [
            { id: "register_hatchery", label: "Register Hatchery", icon: <Plus size={16} /> },
            { id: "create_batch", label: "Create Seed Batch", icon: <Package size={16} /> },
            { id: "upload_health_cert", label: "Upload Certificates", icon: <ShieldCheck size={16} /> }
        ],
        hatchery_tech: [
            { id: "breeding_log", label: "Update Breeding Data", icon: <Activity size={16} /> },
            { id: "larvae_growth", label: "Record Larvae Growth", icon: <CheckCircle size={16} /> },
            { id: "batch_status", label: "Update Batch Status", icon: <ArrowRight size={16} /> }
        ],
        seed_supplier: [
            { id: "check_stock", label: "Check Seed Stocks", icon: <Inbox size={16} /> },
            { id: "manage_orders", label: "Manage Seed Orders", icon: <Package size={16} /> }
        ],
        farmer: [
            { id: "register_farm", label: "Register New Farm", icon: <Plus size={16} /> },
            { id: "add_pond", label: "Add Pond", icon: <Activity size={16} /> },
            { id: "buy_seed", label: "Buy Seed", icon: <Package size={16} /> },
            { id: "schedule_harvest", label: "Schedule Harvest", icon: <Inbox size={16} /> }
        ],
        farm_manager: [
            { id: "feeding_log", label: "Record Feeding", icon: <CheckCircle size={16} /> },
            { id: "water_test_request", label: "Request Water Test", icon: <Activity size={16} /> },
            { id: "report_issue", label: "Report Farm Issue", icon: <AlertTriangle size={16} /> }
        ],
        feed_supplier: [
            { id: "list_inventory", label: "Update Feed Stock", icon: <CheckCircle size={16} /> },
            { id: "track_deliveries", label: "Track Deliveries", icon: <Package size={16} /> }
        ],
        medicine_supplier: [
            { id: "list_products", label: "List Medicines", icon: <Plus size={16} /> },
            { id: "process_orders", label: "Process Orders", icon: <CheckCircle size={16} /> }
        ],
        lab_tech: [
            { id: "upload_report", label: "Upload Test Report", icon: <FileText size={16} /> },
            { id: "schedule_screening", label: "Schedule Screening", icon: <Activity size={16} /> }
        ],
        consultant: [
            { id: "give_advice", label: "Publish Advisory", icon: <FileText size={16} /> },
            { id: "view_farm_logs", label: "View Farm Logs", icon: <Activity size={16} /> }
        ],
        harvest_contractor: [
            { id: "assign_labor", label: "Assign Laborers", icon: <Users size={16} /> },
            { id: "track_machinery", label: "Track Machinery", icon: <Activity size={16} /> }
        ],
        harvest_laborer: [
            { id: "mark_attendance", label: "Mark Attendance", icon: <CheckCircle size={16} /> },
            { id: "view_schedule", label: "View Schedule", icon: <Activity size={16} /> }
        ],
        ice_supplier: [
            { id: "update_ice_stock", label: "Update Ice Stock", icon: <Package size={16} /> },
            { id: "receive_orders", label: "Receive Orders", icon: <Inbox size={16} /> }
        ],
        logistics_provider: [
            { id: "request_transport", label: "Accept Transport", icon: <Package size={16} /> },
            { id: "update_tracking", label: "Update GPS Tracking", icon: <Activity size={16} /> }
        ],
        plant_manager: [
            { id: "processing_start", label: "Start Processing", icon: <Zap size={16} /> },
            { id: "inventory_status", label: "Inventory Status", icon: <Package size={16} /> }
        ],
        qc_inspector: [
            { id: "inspect_batch", label: "Inspect Seafood", icon: <ShieldCheck size={16} /> },
            { id: "issue_certificate", label: "Issue QC Cert", icon: <FileText size={16} /> }
        ],
        cold_storage: [
            { id: "temp_log", label: "Record Temperature", icon: <Activity size={16} /> },
            { id: "space_availability", label: "Update Space", icon: <Plus size={16} /> }
        ],
        local_buyer: [
            { id: "market_bid", label: "Place Market Bid", icon: <ArrowRight size={16} /> },
            { id: "view_suppliers", label: "View Suppliers", icon: <Users size={16} /> }
        ],
        exporter: [
            { id: "export_permits", label: "Apply for Permits", icon: <FileText size={16} /> },
            { id: "shipment_booking", label: "Book Shipment", icon: <Package size={16} /> }
        ],
        retailer: [
            { id: "order_stock", label: "Order Fresh Stock", icon: <Plus size={16} /> },
            { id: "daily_sales", label: "Record Daily Sales", icon: <CheckCircle size={16} /> }
        ],
        government_auth: [
            { id: "issue_license", label: "Issue License", icon: <ShieldCheck size={16} /> },
            { id: "field_audit", label: "Schedule Audit", icon: <Activity size={16} /> }
        ],
        banker: [
            { id: "apply_loan", label: "Review Loan App", icon: <ArrowRight size={16} /> },
            { id: "credit_score", label: "Check Credit Score", icon: <ShieldCheck size={16} /> }
        ],
        insurance_provider: [
            { id: "verify_claim", label: "Verify Claim", icon: <CheckCircle size={16} /> },
            { id: "list_policies", label: "Manage Policies", icon: <FileText size={16} /> }
        ],
        admin: [
            { id: "user_management", label: "Manage Users", icon: <Users size={16} /> },
            { id: "system_health", label: "System Health", icon: <Activity size={16} /> }
        ]
    };

    const availableActions = roleActions[user_info.role] || [];

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Unified Portal Hero */}
            <div className="relative overflow-hidden rounded-[2.5rem] bg-slate-900 border border-white/5 p-8 md:p-12 shadow-2xl">
                <div className="relative z-10">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-8">
                        <div>
                            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-600/10 border border-cyan-600/20 text-cyan-400 text-xs font-black uppercase tracking-[0.2em] mb-6 shadow-inner">
                                <ShieldCheck size={14} />
                                {role_info.category} CONTROL PORTAL
                            </div>
                            <h1 className="text-4xl md:text-6xl font-black text-white mb-4 tracking-tighter text-left">
                                {role_info.icon} {user_info.role_display}
                            </h1>
                            <p className="text-slate-400 text-lg max-w-xl font-medium leading-relaxed text-left">
                                Welcome back, <span className="text-white font-bold">{user_info.name}</span>. Your specialized AquaSphere tools are synced and active.
                            </p>
                        </div>

                        {/* Dynamic Widgets */}
                        <div className="flex gap-4 overflow-x-auto pb-2">
                            {widgets.map((w, i) => (
                                <div key={i} className={`flex-shrink-0 p-6 rounded-3xl bg-${w.color}-500/10 border border-${w.color}-500/20 shadow-xl`}>
                                    <div className={`text-${w.color}-400 text-xs font-black uppercase tracking-widest mb-1`}>{w.label}</div>
                                    <div className="text-white text-3xl font-black">{w.value}</div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Quick Action Bar */}
                    {availableActions.length > 0 && (
                        <div className="mt-12 flex flex-wrap gap-4 pt-8 border-t border-white/5">
                            {availableActions.map(action => (
                                <button
                                    key={action.id}
                                    onClick={() => setActiveActionModal(action.id)}
                                    className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-white/5 border border-white/10 text-white font-bold hover:bg-white/10 hover:border-cyan-500/50 transition-all group"
                                >
                                    <span className="text-cyan-400 group-hover:scale-110 transition-transform">{action.icon}</span>
                                    {action.label}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
                {/* Visual accents */}
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyan-500/5 blur-[120px] -mr-64 -mt-64 rounded-full pointer-events-none"></div>
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/5 blur-[80px] -ml-32 -mb-32 rounded-full pointer-events-none"></div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
                {/* Main Content Area (8/12) */}
                <div className="xl:col-span-8 space-y-8">

                    {/* Role-Specific Data Sections */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Leads & Interactions Section */}
                        <div className="glass-card p-8 space-y-6">
                            <div className="flex items-center justify-between">
                                <h3 className="text-xl font-black text-white flex items-center gap-3">
                                    <Inbox className="text-cyan-400" />
                                    Work Leads
                                </h3>
                                <span className="bg-cyan-500/10 text-cyan-400 text-[10px] font-black px-2 py-0.5 rounded-full border border-cyan-500/20">
                                    {leads.length} SYSTEM
                                </span>
                            </div>

                            <div className="space-y-4">
                                {leads.length > 0 ? leads.map((lead) => (
                                    <div key={lead.id} className="p-5 rounded-2xl bg-white/5 border border-white/5 hover:border-white/10 transition-all group">
                                        <div className="flex justify-between items-start mb-2">
                                            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">ID: {lead.id}</span>
                                            <span className="px-2 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 text-[10px] font-black uppercase">{lead.status}</span>
                                        </div>
                                        <p className="text-white text-sm font-semibold group-hover:text-cyan-400 transition-colors">{lead.msg}</p>
                                    </div>
                                )) : (
                                    <div className="text-center py-10 opacity-30">
                                        <Inbox size={40} className="mx-auto mb-3" />
                                        <p className="text-sm font-bold">No active tasks</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Document Hub section */}
                        <div className="glass-card p-8 space-y-6">
                            <h3 className="text-xl font-black text-white flex items-center gap-3">
                                <FileText className="text-purple-400" />
                                Operational Logs
                            </h3>
                            <div className="space-y-4">
                                {reports.length > 0 ? reports.map((rep) => (
                                    <div key={rep.id} className="p-5 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/[0.07] transition-all flex items-center gap-4 cursor-pointer">
                                        <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400">
                                            <FileText size={20} />
                                        </div>
                                        <div className="text-left">
                                            <div className="text-white text-sm font-bold">{rep.title}</div>
                                            <div className="text-slate-500 text-xs font-medium uppercase tracking-tighter mt-0.5">{rep.date}</div>
                                        </div>
                                    </div>
                                )) : (
                                    <div className="text-center py-10 opacity-30">
                                        <FileText size={40} className="mx-auto mb-3" />
                                        <p className="text-sm font-bold">No logs record</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Unified Connectivity Section */}
                    <div className="glass-card p-8 space-y-8">
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                            <div className="text-left">
                                <h2 className="text-2xl font-black text-white flex items-center gap-3">
                                    <Users className="text-amber-400 shadow-sm" />
                                    Industry Cycle
                                </h2>
                                <p className="text-slate-500 text-xs font-bold uppercase tracking-widest mt-1">Direct Networking Nodes</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {connections.map((conn) => (
                                <motion.div
                                    whileHover={{ scale: 1.03, y: -5 }}
                                    key={conn.id}
                                    className="group p-6 rounded-3xl bg-slate-800/40 border border-white/5 hover:border-amber-500/20 transition-all cursor-pointer relative overflow-hidden"
                                >
                                    <div className="relative z-10 text-left">
                                        <div className="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform mb-4">
                                            {conn.icon}
                                        </div>
                                        <h4 className="text-white font-black group-hover:text-amber-400 transition-colors leading-tight mb-1">{conn.name}</h4>
                                        <p className="text-slate-500 text-[10px] uppercase font-black tracking-[0.15em]">{conn.category}</p>
                                    </div>
                                    <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <ArrowRight size={16} className="text-amber-400" />
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Sidebar: System Intel & Activity (4/12) */}
                <div className="xl:col-span-4 space-y-8">
                    {/* Live Activity Feed */}
                    <div className="glass-card p-8 space-y-6 flex flex-col h-full text-left">
                        <div className="flex items-center justify-between">
                            <h3 className="text-xl font-black text-white flex items-center gap-3">
                                <Activity className="text-emerald-400" />
                                Activity Feed
                            </h3>
                            <div className="flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-emerald-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-400"></span>
                            </div>
                        </div>
                        <div className="flex-1 space-y-6">
                            {recent_activity.map((act, i) => (
                                <div key={i} className="flex gap-5 relative">
                                    <div className="flex flex-col items-center">
                                        <div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                                        {i !== recent_activity.length - 1 && <div className="w-px flex-1 bg-white/5 mt-2"></div>}
                                    </div>
                                    <div className="pb-4">
                                        <p className="text-white text-sm font-bold leading-normal mb-1">{act.msg}</p>
                                        <p className="text-slate-600 text-[10px] font-black uppercase tracking-widest">{act.time}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* ACTION MODAL */}
            <AnimatePresence>
                {activeActionModal && (
                    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="absolute inset-0 bg-black/80 backdrop-blur-sm"
                            onClick={() => setActiveActionModal(null)}
                        />
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            className="relative w-full max-w-md bg-slate-900 rounded-[2.5rem] border border-white/10 p-8 shadow-2xl overflow-hidden"
                        >
                            <div className="flex items-center justify-between mb-8">
                                <h3 className="text-2xl font-black text-white capitalize">
                                    {activeActionModal.replace('_', ' ')}
                                </h3>
                                <button onClick={() => setActiveActionModal(null)} className="p-2 rounded-full hover:bg-white/10 transition-colors text-slate-400">
                                    <X size={24} />
                                </button>
                            </div>

                            <form onSubmit={handleActionSubmit} className="space-y-6">
                                {/* Dynamic Form Fields based on Action */}
                                {activeActionModal.includes('register') ? (
                                    <>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Facility Name</label>
                                            <input name="name" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none transition-all" placeholder="e.g. Royal Blue Hatchery" />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Location</label>
                                            <input name="location" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none transition-all" placeholder="City, Region" />
                                        </div>
                                    </>
                                ) : activeActionModal === "create_batch" ? (
                                    <>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Specie Type</label>
                                            <select name="type" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none transition-all">
                                                <option>Vannamei Shrimp</option>
                                                <option>Black Tiger</option>
                                                <option>Sea Bass</option>
                                            </select>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Count (Millions)</label>
                                                <input name="count" type="number" step="0.1" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none" />
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Price per Unit</label>
                                                <input name="price" type="number" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none" />
                                            </div>
                                        </div>
                                    </>
                                ) : activeActionModal === "upload_report" ? (
                                    <>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Report Title</label>
                                            <input name="title" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none transition-all" placeholder="e.g. Water Quality Analysis #442" />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest">Facility ID</label>
                                            <input name="target_role" required className="w-full bg-slate-800 border border-white/5 rounded-2xl p-4 text-white focus:border-cyan-500 outline-none transition-all" placeholder="F-123 or H-456" />
                                        </div>
                                    </>
                                ) : (
                                    <div className="py-10 text-center opacity-50">Custom logic pending...</div>
                                )}

                                <button
                                    disabled={actionLoading}
                                    type="submit"
                                    className="w-full py-4 rounded-2xl bg-cyan-500 text-black font-black uppercase tracking-widest hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50"
                                >
                                    {actionLoading ? "Processing..." : "Submit Action"}
                                </button>
                            </form>

                            <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 blur-[80px] -mr-32 -mt-32 rounded-full pointer-events-none"></div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Dashboard;
