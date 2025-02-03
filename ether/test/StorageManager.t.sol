pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {StorageManager} from "../src/StorageManager.sol";

contract StorageManagerTest is Test {
    StorageManager public manager;

    function setUp() public {
        manager = new StorageManager();
    }

    function test_setKey() public {
        manager.setKey(0);
    }

    function test() public view {
        assertEq(manager.getKey(), 0);
    }
}