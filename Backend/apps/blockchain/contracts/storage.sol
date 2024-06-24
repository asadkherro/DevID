pragma solidity ^0.8.0;

contract SimpleStorage {
    string[] private values;

    function set(string memory x) public {
        values.push(x);
    }

    function get() public view returns (string[] memory) {
        return values;
    }
}
