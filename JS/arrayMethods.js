function getMax(myArray) {
  n=myArray.length;
  max=0
  for(i=0;i<n;i++){//this function could be made recurisve...
    console.log(i)
    m=myArray[i].length;
    for(ii=0;ii<m;ii++){
      console.log(ii)
      x=myArray[i][ii]
      if(x>max){
        max=x
      }
    }
  }
  return max
}

function getMin(myArray) {
  n=myArray.length;
  min=0
  for(i=0;i<n;i++){//this function could be made recurisve...
    console.log(i)
    m=myArray[i].length;
    for(ii=0;ii<m;ii++){
      if(myArray[i][ii]<min){
        min=myArray[i][ii]
      }
    }
  }
  return min
}

function twoDMax(arr,ind){
  n=arr.length;
  max=0;
  for(i=0;i<n;i++){
    if(arr[i][ind]>max){
      max=arr[i][ind];
    }
  }
  return max
}
function twoDMin(arr,ind){
  n=arr.length;
  min=0;
  for(i=0;i<n;i++){
    if(arr[i][ind]<min){
      min=arr[i][ind];
    }
  }
  return min
}
