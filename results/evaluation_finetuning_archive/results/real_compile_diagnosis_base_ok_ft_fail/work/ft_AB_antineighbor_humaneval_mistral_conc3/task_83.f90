program starts_one_ends
  implicit none
  integer :: n
  integer :: result

  read(*,*) n
  result = starts_one_ends(n)
  print *, result

contains

  function starts_one_ends(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i

    if (n == 1) then
      res = 1
    else
      res = 0
      do i = 10**(n-1), 10**n - 1
        if (i/10**(n-1) == 1 .or. mod(i,10) == 1) then
          res = res + 1
        end if
      end do
    end if
  end function starts_one_ends

end program starts_one_ends