import pandas as pd
import heapq
import math

class Item:
    def __init__(self, id, score, category):
        self.id = id
        self.score = score
        self.category = category

    def __lt__(self, other):
        return self.score < other.score

def TopKSelectionFromSortedList(ListOfItems, K:int, d:int, floorList, ceilList):
    '''
    L : List of items sorted by score
    K : Number of items to select
    d : Number of categories
    Ki = number of items to select from i'th category
    floorList[i] <= ki <= ceilList[i]
    
    Output: ListToReturn
    '''
    
    listToReturn = []
    
    C = [0] * d
    
    total = sum(floorList)
    Slack = K - total

    index = 0
    while len(listToReturn) < K:
        x = ListOfItems[index]
        index += 1
        i = x.category
        
        if C[i] < floorList[i]:
            listToReturn.append(x)
            C[i] += 1
            
        elif C[i] < ceilList[i] and Slack > 0:
            listToReturn.append(x)
            C[i] += 1
            Slack -= 1
        
    return listToReturn

def SecretaryAlgorithm(ListOfItems, K:int, N:int, d:int, floorList, ceilList, numItemsList, warmup_factor = 1, walking_distance = 0):
    listToReturn = []
    C = [0] * d
    M = [0] * d
    R = [math.floor(num / (warmup_factor * math.e)) for num in numItemsList]
    CategoriesMinHeaps = [[] for _ in range(d)]

    slack = K - sum(floorList)
    r = math.floor(N / (warmup_factor * math.e))

    MaxNumOfElementsInHeap = [num for num in floorList]
    MaxNumOfElementsInIndependentHeap = slack

    T = []
    index = 0
    while len(listToReturn) < K:
        x = ListOfItems[index]
        index += 1
        i = x.category
        walking_distance[0] += 1

        if sum(M) < r:
            Offer(T, x, MaxNumOfElementsInIndependentHeap)

        if M[i] < R[i]:
            Offer(CategoriesMinHeaps[i], x, MaxNumOfElementsInHeap[i])
        elif ((C[i] < floorList[i]) and (x.score > getMinElement(CategoriesMinHeaps[i]))) or (numItemsList[i] - M[i] == floorList[i] - C[i]):
            heapq.heappop(CategoriesMinHeaps[i])
            listToReturn.append(x)
            C[i] += 1

        elif (sum(M) >= r) and (x.score > getMinElement(T) and (C[i] < ceilList[i]) and (slack > 0)):
            heapq.heappop(T)
            listToReturn.append(x)
            C[i] += 1
            slack -= 1

        elif (C[i] < ceilList[i]) and (numFeasibleItems(d, C, M, ceilList, numItemsList) == K - len(listToReturn)):
            listToReturn.append(x)
            C[i] += 1
            slack -= 1

        M[i] += 1

    return listToReturn

def Offer(MinHeap, x, maxNumOfElements):
    if maxNumOfElements <= 0:
        return
    if (len(MinHeap) == maxNumOfElements) and (x.score > getMinElement(MinHeap)):
        heapq.heappop(MinHeap)
        heapq.heappush(MinHeap, x)
        return
    
    if len(MinHeap) < maxNumOfElements:
        heapq.heappush(MinHeap, x)

def numFeasibleItems(d, C, M, ceilList, numItemsList):
    sum = 0
    for i in range(d):
        if (ceilList[i] - C[i] > 0):
            sum += (numItemsList[i] - M[i])
    
    return sum

def getMinElement(MinHeap):
    if len(MinHeap) == 0:
        return 0
    return MinHeap[0].score

def process_file(file_path, K:int, d:int, floorList:list, ceilList:list, algorithm_type, N:int, numItemsList:list):
    """
    Reads an Excel file, extracts valid data, and runs the appropriate selection algorithm.

    :param file_path: Excel file path.
    :param K: Total items to pick.
    :param d: Number of categories.
    :param floorList: Min constraints per category.
    :param ceilList: Max constraints per category.
    :param algorithm_type: "static" or "online"
    :return: DataFrame of selected items.
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")

        # Ensure required columns exist
        required_columns = {"ID", "Score", "Category Number"}
        if not required_columns.issubset(df.columns):
            raise ValueError("Excel file must contain 'ID', 'Score', and 'Category Number'.")

        # Convert data types
        df["Score"] = pd.to_numeric(df["Score"], errors="coerce").astype(int)
        df["Category Number"] = pd.to_numeric(df["Category Number"], errors="coerce").astype(int)

        # Adjust category numbers to be 0-based
        df["Category Number"] -= df["Category Number"].min()

        # Sort items by Score for the static problem
        if algorithm_type == "static":
            df_sorted = df.sort_values(by="Score", ascending=False)
        else:  # Online case: Do not sort (items arrive dynamically)
            df_sorted = df

        # Convert DataFrame to list of `Item` objects
        ListOfItems = [Item(row.ID, row.Score, row["Category Number"]) for _, row in df_sorted.iterrows()]

        # Run the appropriate selection function
        if algorithm_type == "static":
            selected_items = TopKSelectionFromSortedList(ListOfItems, K, d, floorList, ceilList)
        else:  # Online problem
            selected_items = SecretaryAlgorithm(ListOfItems=ListOfItems, K=K, N=N, d=d, floorList=floorList, ceilList=ceilList, numItemsList=numItemsList)

        # Convert the list of Item objects into a DataFrame
        selected_df = pd.DataFrame([{"ID": item.id, "Score": item.score, "Category Number": item.category} for item in selected_items])

        return selected_df

    except Exception as e:
        return f"Error: {str(e)}"


def validate_inputs(K, d, floorList, ceilList, df, algorithm_type, N=None, numItemsList=None):
    # 1. Check K constraints
    if K < sum(floorList):
        raise ValueError(f"K={K} is too small. It must be at least sum(floorList)={sum(floorList)}.")
    if K > sum(ceilList):
        raise ValueError(f"K={K} is too large. It must not exceed sum(ceilList)={sum(ceilList)}.")

    # 2. Validate floor and ceil constraints
    for i in range(d):
        if floorList[i] > ceilList[i]:
            raise ValueError(f"Category {i}: floorList[{i}]={floorList[i]} cannot exceed ceilList[{i}]={ceilList[i]}.")

    # 3. Validate file structure
    required_columns = {"ID", "Score", "Category Number"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Excel file must contain 'ID', 'Score', and 'Category Number'.")

    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df["Category Number"] = pd.to_numeric(df["Category Number"], errors="coerce")

    if df["Score"].isna().any():
        raise ValueError("Score column contains NaN or non-numeric values.")
    if df["Category Number"].isna().any():
        raise ValueError("Category Number column contains NaN values.")

    # 4. Validate category counts
    category_counts = df["Category Number"].value_counts().to_dict()
    unique_categories = sorted(category_counts.keys())

    if len(unique_categories) != d:
        raise ValueError(f"Mismatch: File contains {len(unique_categories)} categories, but you specified {d}.")

    for i in range(d):
        if i not in category_counts or category_counts[i] < floorList[i]:
            raise ValueError(f"Category {i}: Needs at least {floorList[i]}, found {category_counts.get(i, 0)}.")

    # 5. Additional checks for online algorithm
    if algorithm_type == "online":
        if N is None or numItemsList is None:
            raise ValueError("For online algorithm, N and numItemsList must be provided.")

        # Ensure N matches the number of rows in the file
        if N != len(df):
            raise ValueError(f"Provided N={N}, but file contains {len(df)} items.")

        # Ensure numItemsList sums to N
        if sum(numItemsList) != N:
            raise ValueError(f"Sum of numItemsList={sum(numItemsList)} does not match N={N}.")

        # Ensure numItemsList[i] matches actual category counts
        for i in range(d):
            actual_count = category_counts.get(i, 0)
            if numItemsList[i] != actual_count:
                raise ValueError(f"Category {i}: Expected {numItemsList[i]} items, but the file contains {actual_count}.")

    return True  # If all checks pass