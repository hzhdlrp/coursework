pragma solidity ^0.8.13;

contract StorageManager {

    mapping(address => int256) private map;

    function setKey(int256 _value) public {
        map[msg.sender] = _value;
    }

    function getKey() public view returns(int256) {
        return map[msg.sender];
    }
}