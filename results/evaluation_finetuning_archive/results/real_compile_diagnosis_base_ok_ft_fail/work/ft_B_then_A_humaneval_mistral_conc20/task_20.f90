program main
      implicit none
      integer :: numbers_len
      real, allocatable :: numbers(:)
      integer :: i, j
      real :: min_diff
      integer :: idx1, idx2

      read *, numbers_len
      allocate(numbers(numbers_len))
      read *, numbers

      min_diff = huge(1.0)
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

      print *, numbers(idx1), numbers(idx2)

      deallocate(numbers)
    end program main