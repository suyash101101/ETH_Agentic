import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import MultiplicationCheckDemo from '../DummyEmbed';

const ZKDemo = () => {
  const { user, logout } = useAuth0();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="bg-black/30 backdrop-blur-md">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="text-2xl font-bold text-white hover:text-cyan-500 transition-colors"
          >
            ← Back to Dashboard
          </button>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <p className="text-white">{user?.name}</p>
            </div>
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
        <div className="bg-white/5 rounded-2xl p-8">
          <h2 className="text-3xl font-bold text-white mb-8">ZK Proof Generator</h2>
          <MultiplicationCheckDemo />
        </div>
      </div>
    </div>
  );
};

export default ZKDemo; 