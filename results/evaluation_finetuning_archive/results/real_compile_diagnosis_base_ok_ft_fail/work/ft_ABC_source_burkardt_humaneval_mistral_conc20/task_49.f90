program modp_demo
  implicit none
  integer :: n, p, result

  ! Read input
  read(*,*) n, p

  ! Compute 2^n mod p
  result = modp(n, p)

  ! Print output
  write(*,*) result

contains

  function modp(n, p) result(res)
    integer, intent(in) :: n, p
    integer :: res
    integer :: i

    res = 1
    do i = 1, n
      res = (res * 2) mod p
    end do
  end function modp

end program modp_demo