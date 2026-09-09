program modp_demo
      implicit none
      integer :: n, p, result

      read(*, *) n
      read(*, *) p
      result = modp(n, p)
      print *, result

    contains

      integer function modp(n, p)
        integer, intent(in) :: n, p
        integer :: base, exp, res
        base = 2
        res = 1
        exp = n
        do while (exp /= 0)
          if (mod(exp, 2) == 1) then
            res = mod(res * base, p)
          end if
          base = mod(base * base, p)
          exp = exp / 2
        end do
        modp = res
      end function modp

    end program modp_demo