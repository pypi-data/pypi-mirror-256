# solidity_testgen

Test generation for Solidity in Foundry format  (https://github.com/foundry-rs/foundry)

Example of Contract under Test:
```
contract C {

    uint x;

	function f(uint _x) public {}
	function g(uint _x, uint _y) public {}
	function w(uint _x) public {}


	function i(uint _x) internal {}
}
```
Expected results of Test Generation:
```
import "forge-std/Test.sol";
import "../src/contract_under_test.sol";

contract contract_under_test_Test is Test {
	C c0, c1, c2, ... cN;

	function setUp() public {
		c0 = new C(); c1 = new C(); ... cN = new C();
	}
	function test_0() public {
		c0.f();
		c0.g();
		....
		c0.w();
	}
........
    function test_n() public {
		cN.g();
		cN.w();
		....
		cN.w();
	}
}
```
### Architecture
![img_2.png](img_2.png)

### Building Tests as CHCs-paths-tree
![img_4.png](img_4.png)


### Dependincies / Setup
* Aeval TestGen (https://github.com/izlatkin/aeval) 
```
git clone https://github.com/izlatkin/aeval
cd aeval
git checkout tg-nonlin
mkdir build ; cd build
cmake ../
cmake --build .  && cmake /home/fmfsu/Dev/blockchain/aeval
make
```
* SMT Encoder set up 
```
git clone https://github.com/leonardoalt/cav_2022_artifact
cd cav_2022_artifact
create a copy of https://raw.githubusercontent.com/ethereum/solc-js/master/smtsolver.ts
remove "solverOutput = execSync ..." section
add line to Dockerfile-solcmc: 
COPY smtsolver_u.ts /home/solc-js/smtsolver.ts
echo "RUN sed -i 's/let solverOutput;/console.log(query); let solverOutput;/g' /home/solc-js/smtsolver.ts" >> Dockerfile-solcmc
docker build -f Dockerfile-solcmc . --rm -t testgen/cav
```

* Solidity Compiler ( > 8.x)
```
npm install -g solc
sudo snap install solc
```

* Foundry (source https://github.com/foundry-rs/foundry)
```
git clone https://github.com/foundry-rs/foundry
cd foundry
cargo install --path ./cli --bins --locked --force
cargo install --path ./anvil --locked --force
```

* LCov
```brew install lcov```
* GenHtml (part or lcov)

used for 
`solc a.sol --ast-compact-json`
example of command
`./docker_solcmc examples smoke_safe.sol Smoke 30 z3`
* ADT 
```
git clone https://github.com/leonardoalt/adt_transform
cd adt_transform 
cargo build
```
location of executable file and example of command
`./target/debug/adt_transform adt_free.smt2`

#### build project
`forge build`

#### run all tests
`forge test`

#### run specified test
`forge test --match Loop*`

#### run test generation for specified sol-file with Python 
`python3 ./scripts/SolidityTestGen.py -i ./src/Loop_1.sol`

#### run test generation for folder with sol-files with Python
`python3 ./scripts/RunAll.py -i folder_path -o ../testgen_output`

#### Report example:
![img_3.png](img_3.png)

#### Generate a report:
`python3 ./scripts/ReportBuilder.py -i testgen_dir`