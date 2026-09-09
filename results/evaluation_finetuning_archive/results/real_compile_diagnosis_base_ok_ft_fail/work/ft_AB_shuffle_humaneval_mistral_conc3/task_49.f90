program modp_demo
  implicit none
  integer :: n, p, result

  ! Read input values
  read(*,*) n
  read(*,*) p

  ! Compute 2^n mod p
  result = modp(n, p)

  ! Print result
  print *, result

contains

  integer function modp(n, p)
    integer, intent(in) :: n, p
    integer :: i, result
    result = 1
    do i = 1, n
      result = (result * 2) mod p
    end do
    modp = result
  end function modp

end program modp_demo