program main
      implicit none
      integer :: n, result
      n = 13195
      result = largest_prime_factor(n)
      print *, result
    contains
      integer function largest_prime_factor(n)
        implicit none
        integer, intent(in) :: n
        integer :: i
        result = 1
        do i = 2, n
          if (mod(n, i) == 0) then
            result = i
            do while (mod(n, i) == 0)
              n = n / i
            end do
          end if
        end do
      end function largest_prime_factor
    end program main