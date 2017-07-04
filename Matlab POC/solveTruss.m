function solveTruss(filename)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%this function will solve trusses
%Based on rewrite of code written by Robert Greenlee
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Open Data File
fid = fopen(filename, 'r');
%% Read Node Data
numberNodes=fscanf(fid,'%d', 1); %Number of nodes
for i=1:numberNodes
    node=fscanf(fid,'%d',1);
    coordinateMatrix(node,1)=fscanf(fid,'%g',1); %Populate a matrix of coordinates
    coordinateMatrix(node,2)=fscanf(fid,'%g',1);
end
%% Read Element Data
numberElements=fscanf(fid,'%d',1);
M=zeros(2*numberNodes,2*numberNodes);
for i=1:numberElements
    element=fscanf(fid,'%d',1);
    nodeFrom=fscanf(fid,'%g',1);
    nodeTo=fscanf(fid,'%g',1);
    
    dx=coordinateMatrix(nodeTo,1)-coordinateMatrix(nodeFrom,1);
    dy=coordinateMatrix(nodeTo,2)-coordinateMatrix(nodeFrom,2);
    length=sqrt(dx^2 + dy^2);
    
    M(2*nodeFrom-1,element)= dx/length;
    M(2*nodeTo-1,element)= -dx/length;
    M(2*nodeFrom,element)= dy/length;
    M(2*nodeTo,element)= -dy/length;
end
%% Read Reaction Data
numberReactions=fscanf(fid,'%d',1);

if(2*numberNodes ~= (numberElements + numberReactions))
    error('Invalid number of nodes, elements, and reactions');
end

for i=1:numberReactions
   reaction=fscanf(fid,'%d',1);
   node=fscanf(fid,'%d',1);
   direction=fscanf(fid,'%s',1);
   
   if ((direction == 'y') | (direction == 'Y'))
        M(2*node, numberElements+reaction)=M(2*node,numberElements+reaction)+1;
   elseif  ((direction=='X') | (direction=='x'))
       M(2*node-1, numberElements+reaction)=M(2*node-1,numberElements+reaction)+1;
   else
       error('Invalid reaction direction')
   end
end
%% Read External Force Data

external=zeros(2*numberNodes,1);
numberForces=fscanf(fid,'%d',1);

for i=1:numberForces
   node=fscanf(fid,'%d',1);
   force=fscanf(fid,'%g',1);
   direction=fscanf(fid,'%g',1);
   
   external(2*node-1)=external(2*node-1)-force*cos(direction*(pi/180));
   external(2*node)=external(2*node)-force*sin(direction*(pi/180));
end
external
%% Compute Forces

A=M\external;

for i=1:numberElements
   fprintf('Element %d = %g \n', i, A(i)) 
end

for i = 1:numberReactions
  fprintf('Reaction %d = %g \n', i, A(numberElements + i))
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end