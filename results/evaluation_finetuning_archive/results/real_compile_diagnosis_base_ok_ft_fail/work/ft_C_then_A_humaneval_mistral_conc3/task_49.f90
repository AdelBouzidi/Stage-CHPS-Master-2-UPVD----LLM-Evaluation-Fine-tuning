program modp
  implicit none
  integer :: n, p, result
  read(*,*) n
  read(*,*) p
  result = modp(n, p)
  print *, result
contains
  integer function modp(n, p)
    integer, intent(in) :: n, p
    integer :: i, res
    res = 1
    do i = 1, n
      res = (res * 2) mod p
    end do
    modp = res
  end function modp
end program modp