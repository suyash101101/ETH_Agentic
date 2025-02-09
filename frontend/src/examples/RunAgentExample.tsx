import { RunAgent } from '../components/RunAgent';

const RunAgentExample = () => {
  return (
    <div>
      <h2>Run Agent Example</h2>
      
      <RunAgent 
        userId="123456"
        agentIndex={0}
        walletId="dc76098f-cb1a-44dd-b628-c1057edc74bd"
        functions={["create_token"]}
      />
    </div>
  );
};

export default RunAgentExample; 