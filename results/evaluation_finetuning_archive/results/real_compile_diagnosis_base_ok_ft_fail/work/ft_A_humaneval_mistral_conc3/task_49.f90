program modp_demo
  implicit none
  integer :: n, p, result

  ! Read input values
  read(*,*) n
  read(*,*) p

  ! Compute 2^n mod p
  result = modp(n, p)

  ! Output result
  print *, result

contains

  integer function modp(n, p)
    integer, intent(in) :: n, p
    integer :: i, result_val
    result_val = 1
    do i = 1, n
      result_val = (result_val * 2) mod p
    end do
    modp = result_val
  end function modp

end program modp_demo