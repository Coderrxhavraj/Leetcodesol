class Solution:
    def trap(self, arr: List[int]) -> int:
        n=len(arr)
        left=0
        right=n-1
        left_max=0
        right_max=0
        water=0
        while left<=right:
            if arr[left]<arr[right]:
                left_max=max(left_max,arr[left])
                water+=left_max-arr[left]
                left+=1
            else:
                right_max=max(right_max,arr[right])
                water+=right_max-arr[right]
                right-=1
        return water