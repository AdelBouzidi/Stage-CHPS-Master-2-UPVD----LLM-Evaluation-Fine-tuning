program main
      implicit none
      integer :: numbers_len
      real, allocatable :: numbers(:)
      integer :: i, j
      real :: min_diff
      integer :: idx1, idx2

      ! Hardcoded input based on the example provided in the prompt
      numbers_len = 6
      allocate(numbers(numbers_len))
      numbers = [1.0, 2.0, 3.0, 4.0, 5.0, 2.2]

      min_diff = huge(0.0)
      idx1 = 1
      idx2 = 2

      do i = 1, numbers_len
        do j = i + 1, numbers_len
          if (abs(numbers(i) - numbers(j)) < min_diff) then
            min_diff = abs(numbers(i) - numbers(j))
            idx1 = i
            idx2 = j
          end if
        end do
      end do

      print *, numbers(min(idx1, idx2)), numbers(max(idx1, idx2))

    end program main