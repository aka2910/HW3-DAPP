// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
    // contract variables
  struct User {
    // struct to store user details
    uint id;
    string name;
  }

  User [] users_list;

  bool last_transaction;

  mapping (uint => uint[][]) public edges;

  function registerUser (uint user_id, string memory user_name) public returns (uint) {
    // function to register a user
    users_list.push(User(user_id, user_name));

    return users_list.length;
  } 

   function registerUser1 () public view returns (uint) {
    // function to check the length of the users_list
    return users_list.length;
  } 

  

  function createAcc(uint user_id_1, uint user_id_2, uint init_bal) public {
    // function to create an account between two users
    edges[user_id_1].push([user_id_2, init_bal]);
    edges[user_id_2].push([user_id_1, init_bal]);
  }

  mapping (uint => bool) public visited;
  mapping (uint => uint) public prev;

  // function dfsUtil(uint user_id_1, uint user_id_2, uint amount) private returns (bool) {
  //   visited[user_id_1] = true;
  //   if (user_id_1 == user_id_2) {
  //       return true;
  //   }
  //   for (uint i = 0; i < edges[user_id_1].length; i++) {
  //       if (!visited[edges[user_id_1][i][0]]) {
  //           if (dfsUtil(edges[user_id_1][i][0], user_id_2, amount)) {
  //               if(edges[user_id_1][i][1] >= amount)  return true;
  //           }
  //       }
  //   }
  //   return false;
  // }

  // function dfsSend( uint user_id_1, uint user_id_2, uint amount) private returns (bool) {
  //   visited[user_id_1] = true;
  //   if (user_id_1 == user_id_2) {
  //       return true;
  //   }
  //   for (uint i = 0; i < edges[user_id_1].length; i++) {
  //       if (!visited[edges[user_id_1][i][0]]) {
  //           if (edges[user_id_1][i][1] >= amount && dfsUtil(edges[user_id_1][i][0], user_id_2, amount)) {
  //                   edges[user_id_1][i][1] -= amount;
  //                   for (uint j = 0; j < edges[user_id_2].length; j++) {
  //                       if (edges[user_id_2][j][0] == user_id_1) {
  //                           edges[user_id_2][j][1] += amount;
  //                           break;
  //                       }
  //                   }
  //                   return true;
  //               }
  //           }
  //       }
  //   return false;
  // }

  // function sendAmount(uint user_id_1, uint user_id_2, uint amount) public returns (bool) {
  //   for(uint i = 0; i < users_list.length; i++) {
  //       visited[users_list[i].id] = false;
  //   }
  //   if (dfsUtil(user_id_1, user_id_2, amount)) {
  //     for(uint i = 0; i < users_list.length; i++) {
  //         visited[users_list[i].id] = false;
  //     }
  //     dfsSend(user_id_1, user_id_2, amount);
  //     last_transaction = true;
  //     return true;      
  //   }
  //   last_transaction = false;
  //   return false;
  // }

  function sendAmount(uint user_id_1, uint user_id_2) public returns (bool) {
    // function to send amount from one user to another
    // bfs
    for(uint i = 0; i < users_list.length; i++) {
        visited[users_list[i].id] = false;
    }
    //bfs
    uint[] memory queue = new uint[](users_list.length);
    uint front = 0;
    uint rear = 0;
    queue[rear++] = user_id_1;
    visited[user_id_1] = true;
    prev[user_id_1] = user_id_1;
    while (front < rear) {
        uint curr = queue[front++];
        for (uint i = 0; i < edges[curr].length; i++) {
            if (!visited[edges[curr][i][0]]) {
                visited[edges[curr][i][0]] = true;
                prev[edges[curr][i][0]] = curr;
                if(edges[curr][i][0] == user_id_2) {
                    uint curr1 = user_id_2;
                    while (curr1 != user_id_1) {
                        for (uint j = 0; j < edges[prev[curr1]].length; j++) {
                            if (edges[prev[curr1]][j][0] == curr1) {
                                if(edges[prev[curr1]][j][1]==0){
                                  last_transaction = false;
                                  return false;
                                }
                                break;
                            }
                        curr1 = prev[curr1];
                        }
                    }
                    curr1 = user_id_2;
                    while (curr1 != user_id_1) {
                        for (uint j = 0; j < edges[prev[curr1]].length; j++) {
                            if (edges[prev[curr1]][j][0] == curr1) {
                                edges[prev[curr1]][j][1] -= 1;
                                break;
                            }
                        }
                        for (uint j = 0; j < edges[curr1].length; j++) {
                            if (edges[curr1][j][0] == prev[curr1]) {
                                edges[curr1][j][1] += 1;
                                break;
                            }
                        }
                        curr1 = prev[curr1];
                    }
                    last_transaction = true;
                    return true;
                    }
                queue[rear++] = edges[curr][i][0];
            }
        }
    }
    last_transaction = false;
    return false;
  }

  function sendAmount1() public view returns (bool){
    // function to check if last transaction was successful or not
    return last_transaction;
  }


  function closeAccount(uint user_id_1, uint user_id_2) public {
    // function to close account of user_id_1 
      for (uint i = 0; i < edges[user_id_1].length; i++) {
          if (edges[user_id_1][i][0] == user_id_2) {
              delete edges[user_id_1][i];
              break;
          }
      }
      for (uint i = 0; i < edges[user_id_2].length; i++) {
          if (edges[user_id_2][i][0] == user_id_1) {
              delete edges[user_id_2][i];
              break;
          }
      }
  }
}
