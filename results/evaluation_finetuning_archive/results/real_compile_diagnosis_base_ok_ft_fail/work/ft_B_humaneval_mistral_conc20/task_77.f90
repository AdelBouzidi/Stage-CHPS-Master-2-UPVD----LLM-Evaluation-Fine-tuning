program iscube
  implicit none
  integer :: a, i
  logical :: result

  read *, a

  result = .false.
  do i = -10000, 10000
    if (i**3 == a) then
      result = .true.
      exit
    end if
  end do

  print *, result
end program iscube