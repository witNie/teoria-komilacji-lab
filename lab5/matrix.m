A = eye(3);
B = zeros(3,4);
C = A .+ B;
print C;

D = eye(4);
D[0, 0] = 42;
#D[1:3, 2:4] = 7; # opcjonalnie dla zainteresowanych
print D;
print D[2, 2];
