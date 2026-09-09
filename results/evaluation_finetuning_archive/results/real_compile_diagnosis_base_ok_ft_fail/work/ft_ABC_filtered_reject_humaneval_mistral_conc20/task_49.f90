program modp
  implicit none
  integer :: n, result
  integer, parameter :: p = 5
  read(*,*) n
  result = modp(n, p)
  print *, result
contains
  integer function modp(n, p)
    integer, intent(in) :: n, p
    integer :: i
    modp = 1
    do i = 1, n
      modp = (modp * 2) mod p
    end do
  end function modp
end program modp