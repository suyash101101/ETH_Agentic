import { motion } from 'framer-motion';
import { Sparkles, Shield, Cpu, ChevronDown } from 'lucide-react';
import LoginButton from './LoginButton';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { 
      staggerChildren: 0.1,
      delayChildren: 0.3
    }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { 
    y: 0, 
    opacity: 1,
    transition: { 
      type: "spring",
      stiffness: 100
    }
  }
};

const Landing = () => {
  return (
    <div className="min-h-screen">
      <section className="min-h-screen flex flex-col items-center justify-center relative px-6">
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60rem] h-[60rem] bg-blue-400/5 rounded-full blur-[180px] pointer-events-none"
        />
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-6"
        >
          <h1 className="text-[6.5rem] font-[600] text-white tracking-tight leading-none font-playfair">
            Block
            <span className="bg-gradient-to-r from-blue-300 to-blue-200 bg-clip-text text-transparent font-[600]">
              Blend
            </span>
          </h1>
          <p className="text-gray-400 text-sm tracking-[0.12em] uppercase font-light font-['Inter']">
            Elevate your applications with AI agents Custom functions and zero-knowledge proofs—
            <br />
            seamlessly bridging Web2 to Web3 in one integration
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-16"
        >
          <LoginButton />
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-30"
        >
          <ChevronDown className="w-5 h-5 text-gray-500" />
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="min-h-screen py-20 px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto text-center"
        >
          <h2 className="text-4xl font-bold text-white mb-8">Who We Are</h2>
          <p className="text-xl text-gray-400 leading-relaxed mb-16 font-['Inter'] font-light">
            We're revolutionizing Web3 integration by providing a unified platform that combines 
            AI-powered agents, zero-knowledge proofs, and customizable blockchain functions into 
            one seamless solution.
          </p>

          <div className="space-y-16">
            {[
              {
                icon: <Cpu className="w-10 h-10 text-blue-400" />,
                title: "AI-Powered Agents",
                description: "Deploy intelligent on-chain agents that automate complex blockchain operations and enhance your dApp's capabilities through advanced AI integration."
              },
              {
                icon: <Shield className="w-10 h-10 text-cyan-400" />,
                title: "Zero-Knowledge Integration",
                description: "Implement privacy-preserving computations with our seamless ZK-proof integration, ensuring data security while maintaining transparency."
              },
              {
                icon: <Sparkles className="w-10 h-10 text-purple-400" />,
                title: "Custom Web3 Functions",
                description: "Create and deploy customizable blockchain functions with our one-step integration process, enabling seamless Web2 to Web3 transformation."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="flex flex-col items-center"
              >
                <div className="bg-gradient-to-br from-white/10 to-white/5 rounded-2xl p-5 mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-semibold text-white mb-4 font-playfair">{feature.title}</h3>
                <p className="text-gray-400 max-w-2xl font-['Inter'] font-light">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>
    </div>
  );
};

export default Landing; 