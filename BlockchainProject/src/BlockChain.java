import java.util.ArrayList;
import com.google.gson.GsonBuilder;

public class BlockChain {
	public static ArrayList<Block> blockchain = new ArrayList<>();
	
	public static Boolean isChainValid() {
		for(int i=1;i<blockchain.size();i++) {
			Block currentBlock=blockchain.get(i);
			Block pastBlock=blockchain.get(i-1);
			
			if(!currentBlock.previousHash.equals(pastBlock.hash)) {
				return false;
			}
			
			
			if(!currentBlock.hash.equals(currentBlock.calculateHash()))  {
				return false;
			}
		}
		
		return true;
	}
	
	public static void main(String[] args) {	
		blockchain.add(new Block("HabíA una vez","0"));
		blockchain.add(new Block("En una serie sobre abogados",blockchain.get(blockchain.size()-1).hash));
		blockchain.add(new Block("Que resolvían misterios",blockchain.get(blockchain.size()-1).hash));
		
		String blockchainJson = new GsonBuilder().setPrettyPrinting().create().toJson(blockchain);		
		System.out.print(blockchainJson);
		
		System.out.print(isChainValid());
	}
}
