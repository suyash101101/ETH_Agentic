import { useAuth0 } from "@auth0/auth0-react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <button 
      onClick={() => loginWithRedirect()}
      className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-lg font-semibold rounded-xl hover:scale-105 transition-all duration-300 shadow-lg shadow-cyan-500/20"
    >
      Get Started
    </button>
  );
};

export default LoginButton; 