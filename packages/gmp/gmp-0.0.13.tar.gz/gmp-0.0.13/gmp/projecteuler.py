def solve(problem):
  with open('./gmp/projecteuler.txt', 'r') as file:
      content = file.read()
  
  data = content.split("\n")
  data_dict = {}
  
  for x in data:
      split_data = x.split(". ")
      if len(split_data) >= 2:
          key = split_data[0]
          value = split_data[1]
          data_dict[key] = value
  
  return data_dict[str(problem)]