from bisect import bisect_left, bisect_right


class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        n = len(nums)

        if n < 4:
            return []

        if n == 4:
            return [nums] if sum(nums) == target else []

        ans = []
        add = ans.append

        # Global pruning
        if nums[0] + nums[1] + nums[2] + nums[3] > target:
            return []

        if nums[-1] + nums[-2] + nums[-3] + nums[-4] < target:
            return []

        # For 4Sum, more than 4 equal copies can never create
        # a new unique quadruplet.
        compressed = []
        for idx, x in enumerate(nums):
            if idx < 4 or x != nums[idx - 4]:
                compressed.append(x)

        nums = compressed
        n = len(nums)

        last1 = nums[-1]
        last2 = nums[-2]
        last3 = nums[-3]

        bl = bisect_left
        br = bisect_right

        i = 0

        while i < n - 3:
            a = nums[i]

            # Duplicate a
            if i > 0 and a == nums[i - 1]:
                i += 1
                continue

            # ----- a pruning -----

            # Even the smallest possible quadruplet is too large.
            if a + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break

            # Even the largest possible quadruplet is too small.
            if a + last1 + last2 + last3 < target:
                # Jump directly to the first possible a.
                min_a = target - last1 - last2 - last3
                ni = bl(nums, min_a, i + 1, n - 3)

                if ni >= n - 3:
                    break

                i = max(i + 1, ni)
                continue

            j = i + 1

            while j < n - 2:
                b = nums[j]

                # Duplicate b
                if j > i + 1 and b == nums[j - 1]:
                    j += 1
                    continue

                # Reduce:
                #
                # a + b + c + d = target
                #
                # c + d = need

                need = target - a - b

                # ----- (a,b) pruning -----

                # Smallest c+d is already too large.
                if nums[j + 1] + nums[j + 2] > need:
                    break

                # Largest c+d is still too small.
                if last1 + last2 < need:
                    # Jump to the first b that can possibly work.
                    min_b = target - a - last1 - last2
                    nj = bl(nums, min_b, j + 1, n - 2)

                    if nj >= n - 2:
                        break

                    j = max(j + 1, nj)
                    continue

                # ----- c + d search -----

                left = j + 1
                right = n - 1

                while left < right:
                    c = nums[left]
                    d = nums[right]
                    pair = c + d

                    if pair < need:
                        # c is too small.
                        # Find the first c that could work
                        # with this d.
                        required_c = need - d
                        left = bl(nums, required_c, left + 1, right + 1)

                    elif pair > need:
                        # d is too large.
                        # Find the last d that could work
                        # with this c.
                        required_d = need - c
                        right = br(nums, required_d, left, right + 1) - 1

                    else:
                        add([a, b, c, d])

                        left += 1
                        right -= 1

                        # Skip duplicate c
                        while left < right and nums[left] == c:
                            left += 1

                        # Skip duplicate d
                        while left < right and nums[right] == d:
                            right -= 1

                j += 1

                # Skip duplicate b
                while j < n - 2 and nums[j] == nums[j - 1]:
                    j += 1

            i += 1

            # Skip duplicate a
            while i < n - 3 and nums[i] == nums[i - 1]:
                i += 1

        return ans