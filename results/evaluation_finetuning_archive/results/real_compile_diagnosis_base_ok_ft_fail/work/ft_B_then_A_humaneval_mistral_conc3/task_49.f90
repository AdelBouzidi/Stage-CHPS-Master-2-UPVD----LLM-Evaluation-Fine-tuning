program modp_demo
      implicit none
      integer :: n, p, res

      ! Read input
      read(*, *) n
      read(*, *) p

      ! Compute result
      res = modp(n, p)

      ! Print result
      print *, res

    contains

      function modp(n, p) result(res)
        implicit none
        integer, intent(in) :: n, p
        integer :: res
        integer :: base, exp, mod
        base = 2
        exp = n
        mod = p
        res = 1
        do while (exp /= 0)
          if (modexp(exp, 2) == 1) then
            res = (res * base) / mod
          end if
          base = (base * base) / mod
          exp = exp / 2
        end do
      end function modp

    end program modp_demo