import { CreateAgent } from '../components/CreateAgent';

const CreateAgentExample = () => {
  return (
    <div>
      <h2>Create Agent Example</h2>
      
      {/* Basic usage */}
      <CreateAgent 
        userId="123456"
        prompt="I want to put web3 into my app which handles financial transcation and also want to inculcate nft minting features for the same"
      />

      {/* With custom styling */}
      
    </div>
  );
};

export default CreateAgentExample; 