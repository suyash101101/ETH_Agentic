import { useAuth0 } from '@auth0/auth0-react';
import { Link, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import Profile from './Profile';

const Dashboard = () => {
  const { logout } = useAuth0();

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="bg-black/30 backdrop-blur-md">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-white">
            BlockBlend
          </div>
          <div className="flex items-center gap-6">
            <button
              onClick={() => logout({ returnTo: window.location.origin })}
              className="px-4 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded-lg transition-all"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-12">
        <Profile />
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            onClick={() => navigate('/zk-demo')}
            className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 p-8 rounded-2xl cursor-pointer hover:scale-105 transition-all duration-300"
          >
            <h3 className="text-2xl font-bold text-white mb-4">ZK Proofs Demo</h3>
            <p className="text-gray-400 mb-6">
              Try our zero-knowledge proof generation and verification system
            </p>
            <button className="px-4 py-2 bg-cyan-500 text-white rounded-lg">
              Launch Demo
            </button>
          </div>

          <div className="bg-white/5 p-8 rounded-2xl">
            <h3 className="text-2xl font-bold text-white mb-4">Smart Contracts</h3>
            <p className="text-gray-400 mb-6">
              Generate and deploy smart contracts using AI
            </p>
            <button className="px-4 py-2 bg-white/10 text-white rounded-lg">
              Coming Soon
            </button>
          </div>

          <div className="bg-white/5 p-8 rounded-2xl">
            <h3 className="text-2xl font-bold text-white mb-4">EigenLayer</h3>
            <p className="text-gray-400 mb-6">
              Monitor and manage your EigenLayer integration
            </p>
            <button className="px-4 py-2 bg-white/10 text-white rounded-lg">
              Coming Soon
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 