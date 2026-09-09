program collatz_odd
      implicit none
      integer, parameter :: i4b = selected_int_kind(9)
      integer(i4b) :: n
      integer(i4b), allocatable :: odd_collatz(:)
      integer(i4b) :: i, j, temp

      ! Read input
      read(*, *) n

      ! Initialize array
      allocate(odd_collatz(0))

      ! Generate Collatz sequence odds
      do
        if (n == 1) then
          odd_collatz = [odd_collatz, 1]
          exit
        end if
        if (mod(n, 2) /= 0) then
          odd_collatz = [odd_collatz, n]
        end if
        if (mod(n, 2) == 0) then
          n = n / 2
        else
          n = 3 * n + 1
        end if
      end do

      ! Sort the array
      do i = 1, size(odd_collatz) - 1
        do j = i + 1, size(odd_collatz)
          if (odd_collatz(i) > odd_collatz(j)) then
            temp = odd_collatz(i)
            odd_collatz(i) = odd_collatz(j)
            odd_collatz(j) = temp
          end if
        end do
      end do

      ! Print output
      write(*, '(100(i4b,1x))') odd_collatz

    end program collatz_odd