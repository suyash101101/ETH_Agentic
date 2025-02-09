import LoginButton from './LoginButton';

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-blue-900">
      <nav className="fixed w-full bg-black/10 backdrop-blur-md">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
            BlockBlend
          </div>
          <LoginButton />
        </div>
      </nav>

      <div className="container mx-auto px-6 pt-32">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-7xl font-bold mb-6 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 text-transparent bg-clip-text">
            Web2 to Web3 Bridge
          </h1>
          <p className="text-xl text-gray-300 mb-12">
            Transform your traditional applications into powerful Web3 solutions with AI-powered tools and zero-knowledge proofs
          </p>
          <button
            className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-lg font-semibold rounded-xl hover:scale-105 transition-all duration-300 shadow-lg shadow-cyan-500/20"
          >
            Get Started
          </button>
        </div>

        <div className="mt-32 grid md:grid-cols-3 gap-8">
          <div className="bg-white/5 backdrop-blur-lg p-8 rounded-2xl hover:transform hover:-translate-y-2 transition-all duration-300">
            <div className="text-5xl mb-4">🔐</div>
            <h3 className="text-xl font-semibold text-white mb-3">Zero Knowledge Proofs</h3>
            <p className="text-gray-400">
              Implement privacy-preserving computations with our ZK toolkit
            </p>
          </div>
          <div className="bg-white/5 backdrop-blur-lg p-8 rounded-2xl hover:transform hover:-translate-y-2 transition-all duration-300">
            <div className="text-5xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold text-white mb-3">AI Integration</h3>
            <p className="text-gray-400">
              Smart contract generation and optimization using AI
            </p>
          </div>
          <div className="bg-white/5 backdrop-blur-lg p-8 rounded-2xl hover:transform hover:-translate-y-2 transition-all duration-300">
            <div className="text-5xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold text-white mb-3">EigenLayer Ready</h3>
            <p className="text-gray-400">
              Enhanced security and scalability with EigenLayer
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing; 