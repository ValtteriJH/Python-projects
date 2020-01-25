Im_on_top_fill_me_with_code_separate_includes = """
using namespace std;

const int SIZE = 4;
const int NEW_VALUE = 2;
const int PRINT_WIDTH = 5;  
const int DEFAULT_GOAL = 2048;


// Adds a single new value to board using rEng and distr for random positioning.
// DONT TOUCH
void newValue(vector<vector<NumberTile>> &board,
               default_random_engine &rEng,
               uniform_int_distribution<int> &distr){
    // Tries to assign NEW_VAl to randomly selected tile. Continues trying until
    // newVal() returns true.
    while(!board.at(distr(rEng)).at(distr(rEng)).setValue(NEW_VALUE));
}

// Initializes the board to size SIZE x SIZE and adds SIZE tiles with NEW_VALUE
// to it through new_value() func after initializing the random engine with
// a seed value.
// DONT TOUCH
void initBoard(vector<vector<NumberTile>> &board,
                default_random_engine &rEng,
                uniform_int_distribution<int> &distr){

    // Initialize the board with SIZE x SIZE empty numbertiles.
    for ( auto y = 0; y < SIZE; y++ ){
        board.push_back({});
        for ( auto x = 0; x < SIZE; x++ ){
            // If you don't want to use pairs, replace "make_pair(y, x)"
            // with "y, x".
            board.at(y).push_back(NumberTile(0, make_pair(y, x), &board));
        }

    }

    // Ask user for the seed value and initialize rEng.
    cout << "Give a seed value or an empty line: ";
    string seed = "";
    getline(cin, seed);

    if(seed == "") {
        // If the user did not give a seed value, use computer time as the seed
        // value.
        rEng.seed(time(NULL));
    } else {
        // If the user gave a seed value, use it.
        rEng.seed(stoi(seed));
    }

    // Add some tiles to the board.
    for ( int i = 0 ; i < SIZE ; ++i ){
        newValue(board, rEng, distr);
    }
}

// Prints the board.
// DONT TOUCH    cout << goal;
void print(vector<vector<NumberTile>> &board){
    // The y isn't actually the y coordinate or some int, but an iterator that
    // is like a vector of NumberTiles.
    for ( auto y : board ){
        // Prints a row of dashes.
        cout << string(PRINT_WIDTH * SIZE + 1, '-') << endl;
        // And then print all cells in the desired width.
        for ( auto x : y ){
            x.print(PRINT_WIDTH);
        }
        // And a line after each row.
        cout << "|" << endl;
    }
    // Print a last row of dashes so that the board looks complete.
    cout << string(PRINT_WIDTH * SIZE + 1, '-') << endl;
}
vector<int> move_values(vector<int> original, bool direction)
{
    // push to left
    vector<int> new_values;
    int memory = 0;

    for (int i : original)
    {
        if (i == 0) //skip zeros
            continue;
        else if (memory == 0)   // check if first in lin
        {
            memory = i;
        }
        else                    //determine the action based on the last two numbers
        {
            if (memory == i)
            {
                new_values.push_back(memory + i);
                memory = 0;
            }else{
            new_values.push_back(memory);
            memory = i;
            }
        }
    }
    if (memory != 0)
    {
        new_values.push_back(memory);
    }
    if (!direction)
        std::reverse(std::begin(new_values), std::end(new_values));
    while (new_values.size() < SIZE){
        new_values.push_back(0);
    }
    return new_values;
}
void move_vertical(bool direction, vector<vector<NumberTile>> &board)
{

    vector<int> value_vector = {0};
    if (true)
    {
        for (int y = 0;y < SIZE;y++) {
            vector<int> value_vector;
            for (int x_1 = 0;x_1<SIZE;x_1++) {
                value_vector.push_back(board.at(x_1).at(y).get_value());
            }

            vector<int> new_values = move_values(value_vector, direction);
            if (!direction)
            {
                std::reverse(std::begin(new_values), std::end(new_values));
            }// last loop layer

            for ( int x = 0; x < SIZE; x++ ){
                // If you don't want to use pairs, replace "make_pair(y, x)"
                // with "y, x".
                board.at(x).at(y) = NumberTile(new_values.at(x), make_pair(x, y), &board);
        //reverse only vector by direction
        //make x vector y vector and value vector and reverse by direction
        }
            //y++;
    }
}
}
void move_lateral(bool direction, vector<vector<NumberTile>> &board)
{

    vector<int> value_vector = {0};
    int y = 0;
    if (true)
    {
        for (vector<NumberTile> x_axis : board) {
            vector<int> value_vector;
            for (NumberTile current : x_axis){
                value_vector.push_back(current.get_value());
            }
            vector<int> new_values = move_values(value_vector, direction);
            if (!direction)
            {
                std::reverse(std::begin(new_values), std::end(new_values));
            }// last loop layer

            for ( int x = 0; x < SIZE; x++ ){
                // If you don't want to use pairs, replace "make_pair(y, x)"
                // with "y, x".
                board.at(y).at(x) = NumberTile(new_values.at(x), make_pair(y, x), &board);
        //reverse only vector by direction
        //make x vector y vector and value vector and reverse by direction
        }
            y++;
    }
    }
}

// A method for moving the tile
void moveTile(string direction, vector<vector<NumberTile>> &board)
{
    if ((direction == "w") || (direction == "s"))
    {
        if (direction == "w"){
            move_vertical(true, board);
    }
        else {
            move_vertical(false, board);
        }
        }
    else if ((direction == "a") || (direction == "d"))
    {
        if (direction == "a")
        {
            move_lateral(true, board);
        } else {
            move_lateral(false, board);
        }
    }
}
int win_lose_check(vector<vector<NumberTile>> &board, int goal)
{
    int zeros = 0;
    for (vector<NumberTile> x : board)
    {
        // std::find(winwangler.begin(), winwangler.end(), goal) != winwangler.end()
        for (NumberTile y : x)
        {
            int i = y.get_value();
            if (i == goal)
            {
                return 1;
            }
            else if (i == 0)
            {
                zeros++;
            }
        }

    }
    if (zeros == 0)
    {
        return -1;
    }
    return 0;
}

int main()
{
    // Declare the board and randomengine.
    vector<vector<NumberTile>> board;
    default_random_engine randomEng;
    // And initialize the disrt to give numbers from the correct
    uniform_int_distribution<int> distr(0, SIZE - 1);

    initBoard(board, randomEng, distr);
    // Ask user for the win condition value, default value is 2048.
    cout << "Give a goal value or an empty line: ";
    int goal;
    string answer;
    getline(cin, answer);
    if (answer == "")
    {
        goal = DEFAULT_GOAL;
    }
    else {
        goal = stoi(answer);
    }
    print(board);

    // endgame stops the game when lost or won.
    bool endgame = false;
    vector<string> commands = {"w","a","s","d","q"};
    bool goodval = false;
    while (!endgame)
        {
        cout << "dir> ";
        string command;
        getline(cin, command);
        for (string i : commands){
            if (command == i){
                goodval = true;
                if (i == "q"){
                    return 0;
                }
                else {
                    moveTile(i, board);
                    if (win_lose_check(board, goal) == 0){
                    newValue(board, randomEng, distr);
                        continue;}
                    else if (win_lose_check(board, goal) == -1){
                        cout << "Can't add new tile, you lost!" << endl;
                        endgame = true;
                    }
                    else {
                        print(board);
                        cout << "You reached the goal value of "<< goal <<"!" << endl;
                        endgame = true;
                    }
                }
            }
        }
        if (!goodval){
            cout << "Error: unknown command." << endl;
        }
        else if (!endgame){
        print(board);
        goodval = false;
        }
}
}

"""
b = Im_on_top_fill_me_with_code_separate_includes.split("\n")
c = "".join(b)
print(c)
