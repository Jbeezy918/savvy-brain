import React from 'react';
import { Bot, Cpu, TerminalSquare, ExternalLink, Activity, Server, Radio, Wrench, MessageSquare, Briefcase, FileText } from 'lucide-react';

const AgentsWorkspace = () => {
  const agents = [
    { name: 'Agent Zero', status: 'RUNNING', cpu: '14%', task: 'Background monitoring', icon: TerminalSquare, url: 'http://localhost:50001', color: 'cyan', provider: 'Qwen 2.5 32B' },
    { name: 'OpenClaw', status: 'IDLE', cpu: '2%', task: 'Awaiting commands', icon: Bot, url: 'http://localhost:8000', color: 'purple', provider: 'Llama 3.1 70B' },
    { name: 'Claude Orchestrator', status: 'PROCESSING', cpu: '82%', task: 'Generating proposal draft', icon: MessageSquare, url: 'http://localhost:3737', color: 'orange', provider: 'Claude 3.5 Sonnet' },
    { name: 'Guardian', status: 'RUNNING', cpu: '5%', task: 'Intrusion detection loop', icon: Server, url: '#', color: 'emerald', provider: 'Local Ruleset' },
    { name: 'Resume Hunter', status: 'SLEEPING', cpu: '0%', task: 'Scheduled for 08:00 UTC', icon: Briefcase, url: '#', color: 'blue', provider: 'DeepSeek Coder' },
    { name: 'SAM Hunter', status: 'RUNNING', cpu: '22%', task: 'Scraping NAICS 541511', icon: FileText, url: '#', color: 'green', provider: 'Qwen 30B' },
    { name: 'YouTube Analyst', status: 'IDLE', cpu: '0%', task: 'Awaiting video URL', icon: YoutubeIcon, url: '#', color: 'red', provider: 'GPT-4o' },
  ];

  return (
    <div className="flex flex-col h-full bg-[#0f1113] p-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between mb-4 bg-[#1a1c1e] p-3 rounded-lg border border-slate-800 shrink-0">
        <div className="flex items-center gap-4">
          <h2 className="text-sm font-black uppercase tracking-widest text-slate-200">Swarm Roster</h2>
          <div className="w-px h-6 bg-slate-800"></div>
          <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
            {agents.filter(a => a.status === 'RUNNING' || a.status === 'PROCESSING').length} Active Nodes
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 overflow-y-auto custom-scrollbar content-start">
        {agents.map((agent) => (
          <AgentCard key={agent.name} {...agent} />
        ))}
      </div>
    </div>
  );
};

// Extracted Youtube icon component since it wasn't imported from lucide
const YoutubeIcon = (props) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17" />
    <path d="m10 15 5-3-5-3z" />
  </svg>
);

const AgentCard = ({ name, status, cpu, task, icon: Icon, url, color, provider }) => {
  const colorMap = {
    cyan: 'text-cyan-400 border-cyan-500/30 bg-cyan-500/5',
    purple: 'text-purple-400 border-purple-500/30 bg-purple-500/5',
    orange: 'text-orange-400 border-orange-500/30 bg-orange-500/5',
    emerald: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/5',
    blue: 'text-blue-400 border-blue-500/30 bg-blue-500/5',
    green: 'text-green-400 border-green-500/30 bg-green-500/5',
    red: 'text-red-400 border-red-500/30 bg-red-500/5',
  };

  const isRunning = status === 'RUNNING' || status === 'PROCESSING';

  return (
    <div className={`flex flex-col p-4 bg-[#1a1c1e] border ${isRunning ? 'border-slate-600' : 'border-slate-800'} rounded-lg transition-all`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg border ${colorMap[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-200 tracking-tight">{name}</h3>
            <div className="text-[9px] font-mono text-slate-500 uppercase tracking-widest">{provider}</div>
          </div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded border ${
            isRunning ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400' : 
            status === 'SLEEPING' ? 'bg-slate-800 border-slate-700 text-slate-500' :
            'bg-yellow-500/10 border-yellow-500/30 text-yellow-500'
          }`}>
            {status}
          </span>
          {isRunning && (
            <div className="flex items-center gap-1 text-[9px] font-mono font-bold text-green-400">
              <Cpu className="w-3 h-3" /> {cpu}
            </div>
          )}
        </div>
      </div>
      
      <div className="bg-[#0f1113] border border-slate-800 p-2 rounded mb-4 flex-1">
        <div className="text-[8px] font-bold text-slate-500 uppercase tracking-widest mb-1">Last / Current Task</div>
        <div className="text-xs font-medium text-slate-300 truncate" title={task}>{task}</div>
      </div>
      
      <div className="flex justify-end pt-3 border-t border-slate-800">
        <a 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="flex items-center gap-2 px-3 py-1.5 bg-[#0f1113] hover:bg-cyan-500/10 hover:text-cyan-400 text-slate-400 border border-slate-700 hover:border-cyan-500/50 rounded transition-colors text-[10px] font-bold uppercase tracking-widest group"
        >
          Open Dashboard <ExternalLink className="w-3 h-3 group-hover:scale-110 transition-transform" />
        </a>
      </div>
    </div>
  );
};

export default AgentsWorkspace;
