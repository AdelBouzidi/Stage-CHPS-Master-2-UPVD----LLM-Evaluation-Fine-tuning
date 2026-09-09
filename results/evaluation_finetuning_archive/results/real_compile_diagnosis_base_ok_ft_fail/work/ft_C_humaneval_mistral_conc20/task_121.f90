program solution
  implicit none
  integer :: n, i, sum, val
  read(*,*) n
  sum = 0
  do i = 1, n
    read(*,*) val
    if (mod(i-1, 2) == 0 .and. mod(val, 2) == 1) then
      sum = sum + val
    end if
  end do
  print *, sum
end program solution