pragma solidity >=0.7.0 <0.8.0;

contract Loyal {

    mapping (address => int256) public balances;
    int256 public offset; // now everyone has 100 tokens by default.
    
    event Transfer(address indexed from, address indexed to, int256 value);
    constructor() public {
        offset = 100;
    } 
   
    function transfer(address to, int256 amount) public {
        require(balances[msg.sender] + offset  >= amount && amount > 0 && to != msg.sender);
        balances[msg.sender]-=amount;
        balances[to]+=amount;
        emit Transfer(msg.sender, to, amount);
   }
   
    function getBalance(address addr) public view returns(int256) {
        return balances[addr] + offset;
    }
   
}